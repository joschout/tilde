
resume(off).
use_packs(0).
sampling_strategy(none).

typed_language(yes).
type(replaceable(comp)).
type(not_replaceable(comp)).
type(worn(machine,comp)).

predict(machine(+machine,-action)).
rmode(replaceable(+X)).
rmode(not_replaceable(+X)).
rmode(worn(+Key,+-X)).
