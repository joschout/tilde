
load(examples).
classes([fix,sendback,ok]).

use_packs(0).
resume(off).
sampling_strategy(none).

typed_language(yes).
type(replaceable(comp)).
type(not_replaceable(comp)).
type(worn(comp)).

rmode(replaceable(+X)).
rmode(not_replaceable(+X)).
rmode(worn(+-X)).

