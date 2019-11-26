% Start Tilde with the command 'loofl(tilde,[1])'

predict(sisy(+hhid,-class)).

tilde_mode(classify).
classes([pos,neg]).
max_lookahead(0).
discretize(equal_freq).
report_timings(on).
use_packs(cf_ilp).
sampling_strategy(none).
minimal_cases(50).
write_predictions([testing,distribution]).
m_estimate(m(2)).
tilde_rst_optimization(no).
exhaustive_lookahead(0).
query_batch_size(50000).

typed_language(yes).
type(eadr(ptid,azart,eatyp)).
type(hhold(hhid,a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12,a13,a14,a15,a16,a17,a18,a19,a20,a21,a22,a23,a24,a25,a26,a27,a28,a29,a30,a31,a32,a33,a34,a35,a35,a37,a38,a39,a40,a41,a42)).
type(padr(ptid,azart,kanton,gbeadmgeb)).
type(parrol(prid,ptid,vvid,prtyp,prtypnr)).
type(part(ptid,hhid,epberuf,eperweart,epgebudat,epsta,eplnamecd,epsexcd,epzivstd)).
type(tfkomp(tkid,vvid,tkbeg,tkend,tkexkzwei,tkstacd,tkleist,tkinkprl,tkinkpre,tktarpra,tkuebvwsysp,tkuebvwsysl,tkprfin,tkdyncd,tkausbcd,tkrauv,tksmed,tkrizucd,tktodleista,tkerlleista,tkrenleista,tkeuleista,tkunfleista)).
type(tfrol(prid,tkid,trteceinal,truntcd,trklauscd,trstafcd,trricd)).
type(vvert(vvid,vvstacd,vvinkzwei,vvbeg,vvend,vvinkprl,vvinkpre,vvwae,vvversart,vvaendart,vvaendat,vvabvb,vvabga,vvstifcd,vvvorscd,vvbvgcd,vveucd)).

type(eq_a1(a1,a1)).
type(eq_a10(a10,a10)).
type(eq_a11(a11,a11)).
type(eq_a12(a12,a12)).
type(eq_a13(a13,a13)).
type(eq_a14(a14,a14)).
type(eq_a15(a15,a15)).
type(eq_a16(a16,a16)).
type(eq_a17(a17,a17)).
type(eq_a18(a18,a18)).
type(eq_a19(a19,a19)).
type(eq_a2(a2,a2)).
type(eq_a20(a20,a20)).
type(eq_a21(a21,a21)).
type(eq_a22(a22,a22)).
type(eq_a23(a23,a23)).
type(eq_a24(a24,a24)).
type(eq_a25(a25,a25)).
type(eq_a26(a26,a26)).
type(eq_a27(a27,a27)).
type(eq_a28(a28,a28)).
type(eq_a29(a29,a29)).
type(eq_a3(a3,a3)).
type(eq_a30(a30,a30)).
type(eq_a31(a31,a31)).
type(eq_a32(a32,a32)).
type(eq_a33(a33,a33)).
type(eq_a34(a34,a34)).
type(eq_a35(a35,a35)).
type(eq_a37(a37,a37)).
type(eq_a38(a38,a38)).
type(eq_a39(a39,a39)).
type(eq_a4(a4,a4)).
type(eq_a40(a40,a40)).
type(eq_a41(a41,a41)).
type(eq_a42(a42,a42)).
type(eq_a5(a5,a5)).
type(eq_a6(a6,a6)).
type(eq_a7(a7,a7)).
type(eq_a8(a8,a8)).
type(eq_a9(a9,a9)).
type(eq_azart(azart,azart)).
type(eq_eatyp(eatyp,eatyp)).
type(eq_epberuf(epberuf,epberuf)).
type(eq_eperweart(eperweart,eperweart)).
type(eq_epgebudat(epgebudat,epgebudat)).
type(eq_eplnamecd(eplnamecd,eplnamecd)).
type(eq_epsexcd(epsexcd,epsexcd)).
type(eq_epsta(epsta,epsta)).
type(eq_epzivstd(epzivstd,epzivstd)).
type(eq_gbeadmgeb(gbeadmgeb,gbeadmgeb)).
type(eq_kanton(kanton,kanton)).
type(eq_prtyp(prtyp,prtyp)).
type(eq_prtypnr(prtypnr,prtypnr)).
type(eq_tkausbcd(tkausbcd,tkausbcd)).
type(eq_tkbeg(tkbeg,tkbeg)).
type(eq_tkdyncd(tkdyncd,tkdyncd)).
type(eq_tkend(tkend,tkend)).
type(eq_tkerlleista(tkerlleista,tkerlleista)).
type(eq_tkeuleista(tkeuleista,tkeuleista)).
type(eq_tkexkzwei(tkexkzwei,tkexkzwei)).
type(eq_tkinkpre(tkinkpre,tkinkpre)).
type(eq_tkinkprl(tkinkprl,tkinkprl)).
type(eq_tkleist(tkleist,tkleist)).
type(eq_tkprfin(tkprfin,tkprfin)).
type(eq_tkrauv(tkrauv,tkrauv)).
type(eq_tkrenleista(tkrenleista,tkrenleista)).
type(eq_tkrizucd(tkrizucd,tkrizucd)).
type(eq_tksmed(tksmed,tksmed)).
type(eq_tkstacd(tkstacd,tkstacd)).
type(eq_tktarpra(tktarpra,tktarpra)).
type(eq_tktodleista(tktodleista,tktodleista)).
type(eq_tkuebvwsysl(tkuebvwsysl,tkuebvwsysl)).
type(eq_tkuebvwsysp(tkuebvwsysp,tkuebvwsysp)).
type(eq_tkunfleista(tkunfleista,tkunfleista)).
type(eq_trklauscd(trklauscd,trklauscd)).
type(eq_trricd(trricd,trricd)).
type(eq_trstafcd(trstafcd,trstafcd)).
type(eq_trteceinal(trteceinal,trteceinal)).
type(eq_truntcd(truntcd,truntcd)).
type(eq_vvabga(vvabga,vvabga)).
type(eq_vvabvb(vvabvb,vvabvb)).
type(eq_vvaendart(vvaendart,vvaendart)).
type(eq_vvaendat(vvaendat,vvaendat)).
type(eq_vvbeg(vvbeg,vvbeg)).
type(eq_vvbvgcd(vvbvgcd,vvbvgcd)).
type(eq_vvend(vvend,vvend)).
type(eq_vveucd(vveucd,vveucd)).
type(eq_vvinkpre(vvinkpre,vvinkpre)).
type(eq_vvinkprl(vvinkprl,vvinkprl)).
type(eq_vvinkzwei(vvinkzwei,vvinkzwei)).
type(eq_vvstacd(vvstacd,vvstacd)).
type(eq_vvstifcd(vvstifcd,vvstifcd)).
type(eq_vvversart(vvversart,vvversart)).
type(eq_vvvorscd(vvvorscd,vvvorscd)).
type(eq_vvwae(vvwae,vvwae)).

rmode(eadr(+Ptid0,-Azart1,-Eatyp2)).
rmode(hhold(+Hhid0,-A11,-A22,-A33,-A44,-A55,-A66,-A77,-A88,-A99,-A1010,-A1111,-A1212,-A1313,-A1414,-A1515,-A1616,-A1717,-A1818,-A1919,-A2020,-A2121,-A2222,-A2323,-A2424,-A2525,-A2626,-A2727,-A2828,-A2929,-A3030,-A3131,-A3232,-A3333,-A3434,-A3535,-A3536,-A3737,-A3838,-A3939,-A4040,-A4141,-A4242)).
rmode(padr(+Ptid0,-Azart1,-Kanton2,-Gbeadmgeb3)).
rmode(parrol(-Prid0,+Ptid1,-Vvid2,-Prtyp3,-Prtypnr4)).
rmode(part(-Ptid0,+Hhid1,-Epberuf2,-Eperweart3,-Epgebudat4,-Epsta5,-Eplnamecd6,-Epsexcd7,-Epzivstd8)).
rmode(tfkomp(+-Tkid0,+Vvid1,-Tkbeg2,-Tkend3,-Tkexkzwei4,-Tkstacd5,-Tkleist6,-Tkinkprl7,-Tkinkpre8,-Tktarpra9,-Tkuebvwsysp10,-Tkuebvwsysl11,-Tkprfin12,-Tkdyncd13,-Tkausbcd14,-Tkrauv15,-Tksmed16,-Tkrizucd17,-Tktodleista18,-Tkerlleista19,-Tkrenleista20,-Tkeuleista21,-Tkunfleista22)).
rmode(tfrol(+Prid0,+-Tkid1,-Trteceinal2,-Truntcd3,-Trklauscd4,-Trstafcd5,-Trricd6)).
rmode(vvert(+Vvid0,-Vvstacd1,-Vvinkzwei2,-Vvbeg3,-Vvend4,-Vvinkprl5,-Vvinkpre6,-Vvwae7,-Vvversart8,-Vvaendart9,-Vvaendat10,-Vvabvb11,-Vvabga12,-Vvstifcd13,-Vvvorscd14,-Vvbvgcd15,-Vveucd16)).

rmode(eq_a1(+X, #[0,1,10,11,13,14,15,17,18,19,2,4,5,6,66,7,8,80,81,82,83,84,85,86,87,88,89,9])).
rmode(eq_a10(+X, #[1,4,8])).
rmode(eq_a11(+X, #[0,10,5,6,7,8,9])).
rmode(eq_a12(+X, #[10,11,12,13,14,15,5,6,7,8,9])).
rmode(eq_a13(+X, #[3,4,5,6,7,8])).
rmode(eq_a14(+X, #[1,2,3])).
rmode(eq_a15(+X, #[1630,1632,3,4364,9784])).
rmode(eq_a16(+X, #[3,44138,44838,48836,88838])).
rmode(eq_a17(+X, #[23,3,618,653,83])).
rmode(eq_a18(+X, #[0,1,3,4,5,7,8,9])).
rmode(eq_a19(+X, #[0,1,10,11,12,13,15,16,17,19,2,23,3,30,38,4,40,44,5,6,7,8,9,99])).
rmode(eq_a2(+X, #[0,18,66,7,88])).
rmode(eq_a20(+X, #[0,1,2,3,5])).
rmode(eq_a21(+X, #[0,1,3,4,5,7,8,9])).
rmode(eq_a22(+X, #[0,56,61,65,71])).
rmode(eq_a23(+X, #[0,105,112,114,116])).
rmode(eq_a24(+X, #[0,1,2,5,8])).
rmode(eq_a25(+X, #[0,3,6,7,8])).
rmode(eq_a26(+X, #[137,15,162,187,225,275,35,350,45,55,65,75,85,95])).
rmode(eq_a27(+X, #[3,b,c,d,e,f,g,h,j,k,m,n,o,p,q])).
rmode(eq_a28(+X, #[0,a,b,c,d,e,f])).
rmode(eq_a29(+X, #[1,3,4,8])).
rmode(eq_a3(+X, #[1,4,7,8])).
rmode(eq_a30(+X, #[0,1,2,3,4,5,6,7,8,9])).
rmode(eq_a31(+X, #[0,1,2,3])).
rmode(eq_a32(+X, #[1,3,4,7,8])).
rmode(eq_a33(+X, #[0,1,2,3,4,5,6,7,8,83,88,9])).
rmode(eq_a34(+X, #[1,3,4,7,8])).
rmode(eq_a35(+X, #[1,3,4,7,8,9])).
rmode(eq_a37(+X, #[1,3,4,7,8])).
rmode(eq_a38(+X, #[1,3,4,7,8])).
rmode(eq_a39(+X, #[1,3,4,8])).
rmode(eq_a4(+X, #[10,11,12,14,15,16,17,18,19,41,44,47,48,66,71,74,77,78,8,80,81,84,87,88,89,98])).
rmode(eq_a40(+X, #[0,1,2,3,4,7,8,9])).
rmode(eq_a41(+X, #[1,3,4,7,8])).
rmode(eq_a42(+X, #[1,3,4,8])).
rmode(eq_a5(+X, #[241,259,274,294,634])).
rmode(eq_a6(+X, #[20,21,22,24,25,26,27,28,29,3,61,63,64,68])).
rmode(eq_a7(+X, #[1,3,4,8])).
rmode(eq_a8(+X, #[30,31,34,38,46])).
rmode(eq_a9(+X, #[1,4,7,8])).
rmode(eq_azart(+X, #[1,3,4,5,6,8,9])).
rmode(eq_eatyp(+X, #[1,2,3,4,5])).
rmode(eq_epberuf(+X, #[55,58,90,92,99])).
rmode(eq_eperweart(+X, #[0,1,2,3])).
rmode(eq_epgebudat(+X, #['a0=_inf<x<=1935_5','a0=1935_5<x<=1944_5','a0=1944_5<x<=1954_5','a0=1954_5<x<=1965_5','a0=1965_5<x<=+inf',a0=null])).
rmode(eq_eplnamecd(+X, #[0,1,2])).
rmode(eq_epsexcd(+X, #[1,2])).
rmode(eq_epsta(+X, #[0,1])).
rmode(eq_epzivstd(+X, #[0,1,2,3,4,5])).
rmode(eq_gbeadmgeb(+X, #[83204,84304,85511,90405,93107])).
rmode(eq_kanton(+X, #[ag,be,lu,sg,zh])).
rmode(eq_prtyp(+X, #[10,11,12,14,15,17,18,6,9])).
rmode(eq_prtypnr(+X, #[0,1,2,3,4])).
rmode(eq_tkausbcd(+X, #[0,1,2,3,4,7,8])).
rmode(eq_tkbeg(+X, #['a1=_inf<x<=1983_5','a1=1983_5<x<=1991_5','a1=1991_5<x<=1995_5','a1=1995_5<x<=1996_5','a1=1996_5<x<=+inf'])).
rmode(eq_tkdyncd(+X, #[0,1,2])).
rmode(eq_tkend(+X, #['a2=_inf<x<=2000_5','a2=2000_5<x<=2005_5','a2=2005_5<x<=2011_5','a2=2011_5<x<=2020_5','a2=2020_5<x<=+inf',a2=null])).
rmode(eq_tkerlleista(+X, #['a8=_inf<x<=4','a8=10000_5<x<=30000_5','a8=30000_5<x<=75669','a8=4<x<=10000_5','a8=75669<x<=+inf'])).
rmode(eq_tkeuleista(+X, #['a10=_inf<x<=0_9','a10=0_9<x<=1217_55','a10=1217_55<x<=3645_65','a10=3645_65<x<=7517','a10=7517<x<=+inf'])).
rmode(eq_tkexkzwei(+X, #[0,1,2,3,4,5])).
rmode(eq_tkinkpre(+X, #['a5=_62_4<x<=24_35','a5=_inf<x<=_62_4','a5=24_35<x<=25001','a5=25001<x<=70000_5','a5=70000_5<x<=+inf',a5=null])).
rmode(eq_tkinkprl(+X, #['a4=_inf<x<=0_05','a4=0_05<x<=84_05','a4=1705_45<x<=+inf','a4=388_45<x<=1705_45','a4=84_05<x<=388_45'])).
rmode(eq_tkleist(+X, #['a3=_2<x<=1_4','a3=_inf<x<=_2','a3=1_4<x<=6352_9','a3=25000_5<x<=+inf','a3=6352_9<x<=25000_5'])).
rmode(eq_tkprfin(+X, #[0,1,2])).
rmode(eq_tkrauv(+X, #[1,2,4,5,6,7,8])).
rmode(eq_tkrenleista(+X, #['a9=_2<x<=1_4','a9=_inf<x<=_2','a9=1_4<x<=2596','a9=2596<x<=9423_6','a9=9423_6<x<=+inf',a9=null])).
rmode(eq_tkrizucd(+X, #[0,1])).
rmode(eq_tksmed(+X, #[1])).
rmode(eq_tkstacd(+X, #[0,1,2])).
rmode(eq_tktarpra(+X, #['a6=_inf<x<=79_95','a6=25001<x<=+inf','a6=2913_4<x<=25001','a6=491_65<x<=2913_4','a6=79_95<x<=491_65',a6=null])).
rmode(eq_tktodleista(+X, #['a7=_112_25<x<=4','a7=_inf<x<=_112_25','a7=10000_5<x<=43494','a7=43494<x<=+inf','a7=4<x<=10000_5'])).
rmode(eq_tkuebvwsysl(+X, #[3000,41,43,45,46])).
rmode(eq_tkuebvwsysp(+X, #[3005,41,43,45,46])).
rmode(eq_tkunfleista(+X, #['a11=_inf<x<=1500','a11=10187_5<x<=26770','a11=1500<x<=10187_5','a11=26770<x<=50837_5','a11=50837_5<x<=+inf'])).
rmode(eq_trklauscd(+X, #[0,1])).
rmode(eq_trricd(+X, #[0,1])).
rmode(eq_trstafcd(+X, #[1,2])).
rmode(eq_trteceinal(+X, #['a12=_inf<x<=28_5','a12=28_5<x<=35_5','a12=35_5<x<=43_5','a12=43_5<x<=52_5','a12=52_5<x<=+inf'])).
rmode(eq_truntcd(+X, #[0,1,2])).
rmode(eq_vvabga(+X, #[10308,13955,15416,17490,3330])).
rmode(eq_vvabvb(+X, #[11082,13696,15024,251618,39965])).
rmode(eq_vvaendart(+X, #[1007,15,2,32,54])).
rmode(eq_vvaendat(+X, #['a17=_inf<x<=1992_5','a17=1992_5<x<=1996_5','a17=1996_5<x<=+inf',a17=null])).
rmode(eq_vvbeg(+X, #['a13=_inf<x<=1985_5','a13=1985_5<x<=1992_5','a13=1992_5<x<=1996_5','a13=1996_5<x<=1997_5','a13=1997_5<x<=+inf',a13=null])).
rmode(eq_vvbvgcd(+X, #[0,1,2,3])).
rmode(eq_vvend(+X, #['a14=_inf<x<=2000_5','a14=2000_5<x<=2003_5','a14=2003_5<x<=2008_5','a14=2008_5<x<=2017_5','a14=2017_5<x<=+inf',a14=null])).
rmode(eq_vveucd(+X, #[0,1])).
rmode(eq_vvinkpre(+X, #['a16=_inf<x<=130','a16=130<x<=18538','a16=18538<x<=39932_5','a16=39932_5<x<=83211_5','a16=83211_5<x<=+inf',a16=null])).
rmode(eq_vvinkprl(+X, #['a15=_inf<x<=23','a15=1999_97<x<=4173','a15=23<x<=904_8','a15=4173<x<=+inf','a15=904_8<x<=1999_97'])).
rmode(eq_vvinkzwei(+X, #[0,1,2,3,4,5])).
rmode(eq_vvstacd(+X, #[4,5])).
rmode(eq_vvstifcd(+X, #[0,1,2])).
rmode(eq_vvversart(+X, #[1,2,3,6])).
rmode(eq_vvvorscd(+X, #[0,1,2,3])).
rmode(eq_vvwae(+X, #[756,954])).


execute(loofl(tilde,[1])).
execute(quit).
