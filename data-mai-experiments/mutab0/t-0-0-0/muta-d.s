% Start Tilde with the command 'loofl(tilde,[1])'

predict(muta_d(+drug,-class)).

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
type(atm_br(drug,atomid,atomtype,charge)).
type(atm_c(drug,atomid,atomtype,charge)).
type(atm_cl(drug,atomid,atomtype,charge)).
type(atm_f(drug,atomid,atomtype,charge)).
type(atm_h(drug,atomid,atomtype,charge)).
type(atm_i(drug,atomid,atomtype,charge)).
type(atm_n(drug,atomid,atomtype,charge)).
type(atm_o(drug,atomid,atomtype,charge)).
type(sbond_1(drug,atomid,atomid)).
type(sbond_2(drug,atomid,atomid)).
type(sbond_3(drug,atomid,atomid)).
type(sbond_4(drug,atomid,atomid)).
type(sbond_5(drug,atomid,atomid)).
type(sbond_7(drug,atomid,atomid)).
type(eq_atomtype(atomtype,atomtype)).
type(eq_charge(charge,charge)).

rmode(atm_br(+Drug0,+-Atomid1,-Atomtype2,-Charge3)).
rmode(atm_c(+Drug0,+-Atomid1,-Atomtype2,-Charge3)).
rmode(atm_cl(+Drug0,+-Atomid1,-Atomtype2,-Charge3)).
rmode(atm_f(+Drug0,+-Atomid1,-Atomtype2,-Charge3)).
rmode(atm_h(+Drug0,+-Atomid1,-Atomtype2,-Charge3)).
rmode(atm_i(+Drug0,+-Atomid1,-Atomtype2,-Charge3)).
rmode(atm_n(+Drug0,+-Atomid1,-Atomtype2,-Charge3)).
rmode(atm_o(+Drug0,+-Atomid1,-Atomtype2,-Charge3)).
rmode(sbond_1(+Drug0,+Atomid1,+-Atomid2)).
rmode(sbond_2(+Drug0,+Atomid1,+-Atomid2)).
rmode(sbond_3(+Drug0,+Atomid1,+-Atomid2)).
rmode(sbond_4(+Drug0,+Atomid1,+-Atomid2)).
rmode(sbond_5(+Drug0,+Atomid1,+-Atomid2)).
rmode(sbond_7(+Drug0,+Atomid1,+-Atomid2)).

rmode(eq_atomtype(+X, #[1,10,14,16,19,194,195,21,22,230,232,25,26,27,28,29,3,31,32,34,35,36,38,40,41,42,45,49,50,51,52,8,92,93,94,95])).
rmode(eq_charge(+X, #['a0=_0_1115<x<=0_049','a0=_0_1255<x<=_0_1115','a0=_inf<x<=_0_1255','a0=0_049<x<=0_1425','a0=0_1425<x<=+inf'])).


execute(loofl(tilde,[1])).
execute(quit).
