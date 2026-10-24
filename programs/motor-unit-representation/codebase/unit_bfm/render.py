"""Render saved, fixed-index trajectories and physical traces, without resimulation."""
import os
os.environ.setdefault('MUJOCO_GL','egl')
import argparse,json
from pathlib import Path
import numpy as np
import mujoco
import imageio.v2 as imageio
from PIL import Image,ImageDraw


def render(path,index,out):
    path=Path(path); out=Path(out); out.parent.mkdir(parents=True,exist_ok=True)
    saved=np.load(path); qpos=saved['qpos'][index]; y=saved['y'][index]
    model=mujoco.MjModel.from_xml_path(str(path.with_suffix('.xml')))
    data=mujoco.MjData(model)
    renderer=mujoco.Renderer(model,height=480,width=640)
    camera=mujoco.MjvCamera(); camera.azimuth=90; camera.elevation=-8; camera.distance=1.8
    camera.lookat[:]=[0,0,.7]
    with imageio.get_writer(out,fps=25,codec='libx264',quality=7) as video:
        for t in range(0,len(qpos),4):
            data.qpos[:]=qpos[t]; mujoco.mj_forward(model,data)
            center=(data.xipos[model.body('P').id]+data.xipos[model.body('D').id])/2
            camera.lookat[:]=center
            renderer.update_scene(data,camera=camera)
            frame=Image.fromarray(renderer.render().copy()); draw=ImageDraw.Draw(frame)
            draw.rectangle((0,0,640,50),fill=(20,20,20))
            label=f'SIM_PRIVILEGED  {path.stem}  case={index}  t={(t+1)*.01:.2f}s'
            draw.text((10,5),label,fill='white')
            draw.text((10,25),f'q={y[t,0]*1.2:+.3f}  dq={y[t,1]*6:+.2f}  torque={y[t,12]*6:+.2f}  u={y[t,13]:+.2f}',fill='white')
            video.append_data(np.asarray(frame))
    renderer.close()
    import matplotlib
    matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    fig,axes=plt.subplots(4,1,figsize=(9,8),sharex=True)
    t=(np.arange(len(y))+1)*.01
    for ax,col,scale,label in zip(axes,[0,1,12,13],[1.2,6,6,1],['q [rad]','dq [rad/s]','torque [Nm]','command u']):
        ax.plot(t,y[:,col]*scale); ax.set_ylabel(label); ax.grid(alpha=.25)
    target=None
    if 'q_target' in saved:
        target=saved['q_target'][index]
    elif 'targets' in saved and path.stem in ('goal_result','reward_query'):
        target=np.full(len(y),saved['targets'][index])
    elif 'alpha' in saved and saved['alpha'][index,0]==0:
        target=np.full(len(y),saved['alpha'][index,1])
    if target is not None and np.isfinite(target).any():
        axes[0].plot(t,target,'--',label='requested q'); axes[0].legend(loc='best')
    axes[-1].set_xlabel('time [s]'); fig.suptitle(f'SIM_PRIVILEGED {path.stem} case {index}')
    fig.tight_layout(); fig.savefig(out.with_suffix('.png'),dpi=140); plt.close(fig)


def main():
    p=argparse.ArgumentParser(); p.add_argument('--trajectory',required=True); p.add_argument('--index',type=int,default=0)
    p.add_argument('--out',required=True); a=p.parse_args(); render(a.trajectory,a.index,a.out)

if __name__=='__main__': main()
