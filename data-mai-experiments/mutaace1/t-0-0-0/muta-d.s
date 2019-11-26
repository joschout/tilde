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
type(atom_br(drug,atomid,atmnum,charge)).
type(atom_c(drug,atomid,atmnum,charge)).
type(atom_cl(drug,atomid,atmnum,charge)).
type(atom_f(drug,atomid,atmnum,charge)).
type(atom_h(drug,atomid,atmnum,charge)).
type(atom_i(drug,atomid,atmnum,charge)).
type(atom_n(drug,atomid,atmnum,charge)).
type(atom_o(drug,atomid,atmnum,charge)).
type(atom_s(drug,atomid,atmnum,charge)).
type(sbond_1(drug,atomid,atomid)).
type(sbond_2(drug,atomid,atomid)).
type(sbond_3(drug,atomid,atomid)).
type(sbond_4(drug,atomid,atomid)).
type(sbond_5(drug,atomid,atomid)).
type(sbond_7(drug,atomid,atomid)).
type(eq_atmnum(atmnum,atmnum)).
type(eq_charge(charge,charge)).

rmode(atom_br(+Drug0,+-Atomid1,-Atmnum2,-Charge3)).
rmode(atom_c(+Drug0,+-Atomid1,-Atmnum2,-Charge3)).
rmode(atom_cl(+Drug0,+-Atomid1,-Atmnum2,-Charge3)).
rmode(atom_f(+Drug0,+-Atomid1,-Atmnum2,-Charge3)).
rmode(atom_h(+Drug0,+-Atomid1,-Atmnum2,-Charge3)).
rmode(atom_i(+Drug0,+-Atomid1,-Atmnum2,-Charge3)).
rmode(atom_n(+Drug0,+-Atomid1,-Atmnum2,-Charge3)).
rmode(atom_o(+Drug0,+-Atomid1,-Atmnum2,-Charge3)).
rmode(atom_s(+Drug0,+-Atomid1,-Atmnum2,-Charge3)).
rmode(sbond_1(+Drug0,+Atomid1,+-Atomid2)).
rmode(sbond_2(+Drug0,+Atomid1,+-Atomid2)).
rmode(sbond_3(+Drug0,+Atomid1,+-Atomid2)).
rmode(sbond_4(+Drug0,+Atomid1,+-Atomid2)).
rmode(sbond_5(+Drug0,+Atomid1,+-Atomid2)).
rmode(sbond_7(+Drug0,+Atomid1,+-Atomid2)).

rmode(eq_atmnum(+X, #[c0_1,c0_10,c0_14,c0_16,c0_19,c0_194,c0_195,c0_21,c0_22,c0_230,c0_232,c0_25,c0_26,c0_27,c0_28,c0_29,c0_3,c0_31,c0_32,c0_34,c0_35,c0_36,c0_38,c0_40,c0_41,c0_42,c0_45,c0_49,c0_50,c0_51,c0_52,c0_72,c0_8,c0_92,c0_93,c0_94,c0_95])).
rmode(eq_charge(+X, #['c2_a0=_0_1115<x<=0_049','c2_a0=_0_1265<x<=_0_1115','c2_a0=_inf<x<=_0_1265','c2_a0=0_049<x<=0_1425','c2_a0=0_1425<x<=+inf'])).


execute(loofl(tilde,[1])).
execute(quit).
