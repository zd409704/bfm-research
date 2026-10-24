"""Independent CPU oracle for identical millisecond actuator and wrench semantics."""
import numpy as np
import mujoco


class CPUUnit:
    def __init__(self,model,data,structure,state):
        self.model,self.data,self.structure=model,data,structure
        self.s={name:np.array(value,copy=True) for name,value in state.items()}
        self.p,self.d=(model.body(n).id for n in ('P','D'))
        self.motor=int(model.joint('motor').dofadr[0])
        self.work=np.zeros(2)

    def step(self,u):
        m,d,s=self.model,self.data,self.s
        previous=float(s['u']); s['u']=np.clip(float(u),-1,1)
        wrench=np.zeros((2,3)); contacts=np.zeros(2); self.work[:]=0
        dt=m.opt.timestep
        for _ in range(round(.01/dt)):
            mujoco.mj_forward(m,d)
            tick=int(s['clock']); t=tick*dt
            d.qfrc_applied[:]=0; d.xfrc_applied[:]=0
            s['ring'][tick%len(s['ring'])]=6*s['u']
            target=np.clip(s['ring'][(tick-int(s['delay']))%len(s['ring'])],-s['cap'],s['cap'])
            s['tau']=s['tau']+(1-np.exp(-dt/s['tm']))*(target-s['tau'])
            d.qfrc_applied[self.motor]=s['tau']
            power=s['tau']*d.qvel[self.motor]
            self.work+=np.array([max(power,0),min(power,0)])*dt
            if self.structure.role==1:
                support=s['support']
                f=np.array([-support[0]*d.qpos[0]-support[3]*d.qvel[0],0,
                            -support[1]*d.qpos[1]-support[4]*d.qvel[1]+support[6]])
                moment=np.cross(d.xpos[self.p]-d.xipos[self.p],f)
                moment[1]+=-support[2]*d.qpos[2]-support[5]*d.qvel[2]
                d.xfrc_applied[self.p]=np.r_[f,moment]
            for start,duration,fx,fz,my,fraction,side in s['pulses']:
                phase=t-start
                if 0<=phase<duration:
                    env=min(phase/.05,(duration-phase)/.05,1)
                    env=.5-.5*np.cos(np.pi*env)
                    b=self.p if side<.5 else self.d
                    length=self.structure.lp if side<.5 else self.structure.ld
                    point=d.xpos[b]+d.xmat[b].reshape(3,3)@np.array([0,0,-length*fraction])
                    force=env*np.array([fx,0,fz])
                    moment=np.cross(point-d.xipos[b],force)+np.array([0,env*my,0])
                    d.xfrc_applied[b]+=np.r_[force,moment]
            if self.structure.role==3:
                for side,joint in enumerate(('q1','q3')):
                    j=int(m.joint(joint).dofadr[0]); amp,freq,phase=s['peripheral'][side]
                    q=amp*np.sin(freq*t+phase); v=amp*freq*np.cos(freq*t+phase)
                    d.qfrc_applied[j]=np.clip(8*(q-d.qpos[j])+.5*(v-d.qvel[j]),-3.6,3.6)
            mujoco.mj_step(m,d)
            for side,b in enumerate((self.p,self.d)):
                wrench[side]+=d.xfrc_applied[b,[0,2,4]]*(dt/.01)
            for ci in range(d.ncon):
                c=d.contact[ci]; b0,b1=m.geom_bodyid[c.geom]
                if {b0,b1}=={self.p,self.d}: continue
                f6=np.empty(6); mujoco.mj_contactForce(m,d,ci,f6)
                force=c.frame.reshape(3,3).T@f6[:3]
                torque=c.frame.reshape(3,3).T@f6[3:]
                for side,b in enumerate((self.p,self.d)):
                    sign=(1 if b1==b else -1 if b0==b else 0)
                    if sign:
                        f=sign*force
                        moment=sign*torque+np.cross(c.pos-d.xipos[b],f)
                        wrench[side]+=(dt/.01)*np.array([f[0],f[2],moment[1]])
                        contacts[side]=1
            s['clock']=tick+1
        mujoco.mj_forward(m,d)
        o=np.zeros(24,np.float32)
        q=d.qpos[self.motor]
        o[:2]=[q/1.2,d.qvel[self.motor]/6]
        for side,b in enumerate((self.p,self.d)):
            rot=d.xmat[b].reshape(3,3)
            cv=d.cvel[b]; offset=d.xipos[b]-d.subtree_com[m.body_rootid[b]]
            v=cv[3:]+np.cross(cv[:3],offset)
            o[2+side*5:7+side*5]=[rot[0,2],rot[0,0],v[0]/2,v[2]/2,cv[1]/6]
        o[12:14]=[s['tau']/6,s['u']]; o[14:16]=contacts
        o[16:18]=[(q+1.2)/2.4,(1.2-q)/2.4]
        o[18:]= (wrench/np.array([20.,20.,6.])).flatten()
        return np.r_[o,float(s['u'])-previous].astype(np.float32)

    @classmethod
    def from_gpu(cls,env,world=0):
        m,d=env.cpu_copy(world)
        state={name:env.tensors[name][world].cpu().numpy() for name in
               ('u','tau','cap','tm','delay','clock','ring','support','pulses','peripheral')}
        return cls(m,d,env.structure,state)
