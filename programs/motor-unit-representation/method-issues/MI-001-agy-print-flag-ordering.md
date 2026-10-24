# MI-001: `agy -p` Flag Ordering Regression

**Observed**: `agy -p --effort high ... < prompt.txt` fails with:
`Error: -p took "--effort" as its prompt, so the intended prompt was left as an argument and ignored.`

**Working invocation**:
```
agy --effort high --dangerously-skip-permissions --add-dir /srv/claude -p="$(cat prompts/...txt)"
```

**Impact**: Roster template in `roster.md` updated for subsequent packets.
**Filed**: Packet B01 Step 4 attempt1.
