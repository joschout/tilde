% Start Tilde with the command 'loofl(tilde,[1])'

predict(uwcse(+key,-class)).

root((uwcse(X,Y), kmap(X,_,_))).

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

confidence_level(0.95).

typed_language(yes).
type(courselevel(course,level)).
type(phase(human,phase)).
type(position(human,faculty)).
type(professor(human)).
type(projectmember(project,human)).
type(publication(ref,human)).
type(student(human)).
type(ta(course,human)).
type(taughtby(course,human)).
type(tempadvisedby(human,human)).
type(yearsinprogram(human,years)).
type(kmap(key,human,human)).

type(eq_faculty(faculty,faculty)).
type(eq_level(level,level)).
type(eq_phase(phase,phase)).
type(eq_years(years,years)).

rmode(courselevel(+Course0,-Level1)).
rmode(phase(+Human0,-Phase1)).
rmode(position(+Human0,-Faculty1)).
rmode(professor(+Human0)).
rmode(projectmember(+-Project0,+Human1)).
rmode(projectmember(+Project0,+-Human1)).
rmode(publication(+-Ref0,+Human1)).
rmode(publication(+Ref0,+-Human1)).
rmode(student(+Human0)).
rmode(ta(+-Course0,+Human1)).
rmode(ta(+Course0,+-Human1)).
rmode(taughtby(+-Course0,+Human1)).
rmode(taughtby(+Course0,+-Human1)).
rmode(tempadvisedby(+Human0,+-Human1)).
rmode(tempadvisedby(+-Human0,+Human1)).
rmode(yearsinprogram(+Human0,-Years1)).

rmode(eq_faculty(+X, #[c2_faculty_8,c2_faculty_adjunct_8,c2_faculty_affiliate_8,c2_faculty_emeritus_8,c2_faculty_visiting_8])).
rmode(eq_level(+X, #[c4_level_100_7,c4_level_300_7,c4_level_400_7,c4_level_500_7])).
rmode(eq_phase(+X, #[c5_post_generals_9,c5_post_quals_9,c5_pre_quals_9])).
rmode(eq_years(+X, #[c8_1,c8_10,c8_12,c8_2,c8_3,c8_4,c8_5,c8_6,c8_7,c8_8,c8_9])).


execute(loofl(tilde,[1])).
execute(quit).
