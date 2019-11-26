
predict(bongard(+pic,-class)).

talking(3).
use_packs(0).
resume(off).
sampling_strategy(none).
heuristic(gain).

use_packs(0).
minfreq(0.2).

typed_language(yes).
type(triangle(pic,obj)).
type(square(pic,obj)).
type(circle(pic,obj)).
type(in(pic,obj,obj)).
type(config(pic,obj,conf)).

rmode(5: triangle(+P,+-S)).
rmode(5: square(+P,+-S)).
rmode(5: circle(+P,+-S)).
rmode(5: in(+P,+S1,+-S2)).
rmode(5: config(+P,+S,#[up,down])).
