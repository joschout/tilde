
classes([pos,neg]).

load(examples).
use_packs(0).

typed_language(yes).
type(triangle(obj)).
type(square(obj)).
type(circle(obj)).
type(in(obj,obj)).
type(config(obj,conf)).

rmode(triangle(+-S)).
rmode(square(+-S)).
rmode(circle(+-S)).
rmode(in(+S1,+-S2)).
rmode(config(+S,#[up,down])).

