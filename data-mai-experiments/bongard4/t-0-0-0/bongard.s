% Start Tilde with the command 'loofl(tilde,[1])'

predict(bongard(+pic,-class)).

tilde_mode(classify).
classes([pos,neg]).
max_lookahead(0).
discretize(equal_freq).
report_timings(on).
use_packs(cf_ilp).
sampling_strategy(none).
minimal_cases(2).
write_predictions([testing,distribution]).
m_estimate(m(2)).
tilde_rst_optimization(no).
exhaustive_lookahead(0).
query_batch_size(50000).

typed_language(yes).
type(circle(pic,obj)).
type(config(pic,obj,dir)).
type(eastof(pic,obj,obj)).
type(inside(pic,obj,obj)).
type(northof(pic,obj,obj)).
type(square(pic,obj)).
type(triangle(pic,obj)).
type(eq_dir(dir,dir)).

rmode(circle(+Pic0,+-Obj1)).
rmode(config(+Pic0,+Obj1,-Dir2)).
rmode(eastof(+Pic0,+Obj1,-Obj2)).
rmode(eastof(+Pic0,-Obj1,+Obj2)).
rmode(inside(+Pic0,+Obj1,-Obj2)).
rmode(inside(+Pic0,-Obj1,+Obj2)).
rmode(northof(+Pic0,+Obj1,-Obj2)).
rmode(northof(+Pic0,-Obj1,+Obj2)).
rmode(square(+Pic0,+-Obj1)).
rmode(triangle(+Pic0,+-Obj1)).

rmode(eq_dir(+X, #[down,up])).


execute(loofl(tilde,[1])).
execute(quit).
