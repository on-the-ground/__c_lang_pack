# Guarded Conditional Recursion

> **Status:** public authoring explanation; no independent language authority.

Some workflows discover the next step only after inspecting a Value. An
effect-free selector chooses one structural branch, which can request another
step of the same Goal.

```subsea
root CountDown/1
CountDown = [n] -1> [n <= 0, {true: Finish[n], false: CountDown[n - 1]}]
Finish = (n) -> n
```

Unselected work does not run. Recursion needs a guarded exit; selected steps are
fresh work, so recursive definitions do not imply a cyclic realized Cable.
A valid recursive definition may still not terminate for a particular input.
Use a supported resource or cancellation profile when bounded completion matters.
Syntax does not promise tail-call optimization or unlimited execution. See
[Language Reference](LANGUAGE_REFERENCE.md),
[Runtime Contract](implementation/RUNTIME_CONTRACT.md), and
[Runtime availability](RUNTIME_STATUS.md).
