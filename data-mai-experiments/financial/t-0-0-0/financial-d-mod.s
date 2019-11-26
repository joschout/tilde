% Start Tilde with the command 'loofl(tilde,[1])'

predict(financial_d(+key,-class)).

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
type(account(key,district_id,frequency,date)).
type(card(key,disp_id,card_type,date)).
type(client(key,client_id,birth,district_id)).
type(disp(key,disp_id,client_id,disp_type)).
type(district(district_id,district_name,region,inhabitants,mun1,mun2,mun3,mun4,cities,ratio,avgsal,unemploy95,unemploy96,enterpreneurs,crimes95,crimes96)).
type(loan(key,date,amount,duration,payments)).
type(order(key,bank_to,amount,symbol)).
type(trans(key,date,trans_type,operation,amount,balance,trans_char)).
type(eq_amount(amount,amount)).
type(eq_avgsal(avgsal,avgsal)).
type(eq_balance(balance,balance)).
type(eq_bank_to(bank_to,bank_to)).
type(eq_card_type(card_type,card_type)).
type(eq_cities(cities,cities)).
type(eq_crimes95(crimes95,crimes95)).
type(eq_crimes96(crimes96,crimes96)).
type(eq_disp_type(disp_type,disp_type)).
type(eq_district_name(district_name,district_name)).
type(eq_duration(duration,duration)).
type(eq_enterpreneurs(enterpreneurs,enterpreneurs)).
type(eq_frequency(frequency,frequency)).
type(eq_inhabitants(inhabitants,inhabitants)).
type(eq_mun1(mun1,mun1)).
type(eq_mun2(mun2,mun2)).
type(eq_mun3(mun3,mun3)).
type(eq_mun4(mun4,mun4)).
type(eq_operation(operation,operation)).
type(eq_payments(payments,payments)).
type(eq_ratio(ratio,ratio)).
type(eq_region(region,region)).
type(eq_symbol(symbol,symbol)).
type(eq_trans_char(trans_char,trans_char)).
type(eq_trans_type(trans_type,trans_type)).
type(eq_unemploy95(unemploy95,unemploy95)).
type(eq_unemploy96(unemploy96,unemploy96)).

rmode(account(+Key0,+-District_id1,-Frequency2,+-Date3)).
rmode(card(+Key0,+-Disp_id1,-Card_type2,+-Date3)).
rmode(client(+Key0,+-Client_id1,+-Birth2,+-District_id3)).
rmode(disp(+Key0,+-Disp_id1,+-Client_id2,-Disp_type3)).
rmode(district(+District_id0,-District_name1,-Region2,-Inhabitants3,-Mun14,-Mun25,-Mun36,-Mun47,-Cities8,-Ratio9,-Avgsal10,-Unemploy9511,-Unemploy9612,-Enterpreneurs13,-Crimes9514,-Crimes9615)).
rmode(loan(+Key0,+-Date1,-Amount2,-Duration3,-Payments4)).
rmode(order(+Key0,-Bank_to1,-Amount2,-Symbol3)).
rmode(trans(+Key0,+-Date1,-Trans_type2,-Operation3,-Amount4,-Balance5,-Trans_char6)).

rmode(eq_amount(+X, #['a13=_inf<x<=38772','a13=155028<x<=+inf','a13=38772<x<=68952','a13=68952<x<=93288','a13=93288<x<=155028','a16=_inf<x<=1292','a16=1292<x<=3018_35','a16=3018_35<x<=4379_85','a16=4379_85<x<=6822_5','a16=6822_5<x<=+inf','a17=_inf<x<=132_25','a17=132_25<x<=1973','a17=13932_5<x<=+inf','a17=1973<x<=5613_6','a17=5613_6<x<=13932_5'])).
rmode(eq_avgsal(+X, #['a7=_inf<x<=8402_5','a7=8402_5<x<=8691_5','a7=8691_5<x<=8966_5','a7=8966_5<x<=9637','a7=9637<x<=+inf'])).
rmode(eq_balance(+X, #['a18=_inf<x<=25048_7','a18=25048_7<x<=35687_1','a18=35687_1<x<=47669_9','a18=47669_9<x<=66077_4','a18=66077_4<x<=+inf'])).
rmode(eq_bank_to(+X, #[ab,cd,ef,gh,ij,kl,mn,op,qr,st,uv,wx,yz])).
rmode(eq_card_type(+X, #[classic,gold,junior])).
rmode(eq_cities(+X, #['a5=_inf<x<=4_5','a5=4_5<x<=5_5','a5=5_5<x<=6_5','a5=6_5<x<=8_5','a5=8_5<x<=+inf'])).
rmode(eq_crimes95(+X, #['a11=_inf<x<=1847_5','a11=1847_5<x<=2646_5','a11=2646_5<x<=3694','a11=3694<x<=5089','a11=5089<x<=+inf'])).
rmode(eq_crimes96(+X, #['a12=_inf<x<=1906_5','a12=1906_5<x<=2758_5','a12=2758_5<x<=3635_5','a12=3635_5<x<=5024_5','a12=5024_5<x<=+inf'])).
rmode(eq_disp_type(+X, #[disponent,owner])).
rmode(eq_district_name(+X, #[benesov,beroun,blansko,breclav,brno_mesto,brno_venkov,bruntal,ceska_lipa,ceske_budejovice,cesky_krumlov,cheb,chomutov,chrudim,decin,frydek_mistek,havlickuv_brod,hl_m_praha,hodonin,hradec_kralove,jablonec_n_nisou,jesenik,jicin,jindrichuv_hradec,karlovy_vary,karvina,kladno,kolin,kromeriz,kutna_hora,litomerice,louny,melnik,most,nachod,novy_jicin,nymburk,olomouc,opava,ostrava_mesto,pardubice,pelhrimov,pisek,plzen_jih,plzen_mesto,plzen_sever,prachatice,praha_vychod,praha_zapad,prerov,pribram,prostejov,rakovnik,rokycany,rychnov_nad_kneznou,semily,sokolov,strakonice,sumperk,svitavy,tabor,tachov,teplice,trebic,trutnov,uherske_hradiste,usti_nad_labem,usti_nad_orlici,vsetin,vyskov,zdar_nad_sazavou,zlin,znojmo])).
rmode(eq_duration(+X, #['a14=_inf<x<=18','a14=18<x<=30','a14=30<x<=42','a14=42<x<=54','a14=54<x<=+inf'])).
rmode(eq_enterpreneurs(+X, #['a10=_inf<x<=101','a10=101<x<=109_5','a10=109_5<x<=118_5','a10=118_5<x<=130_5','a10=130_5<x<=+inf'])).
rmode(eq_frequency(+X, #[poplatek_mesicne,poplatek_po_obratu,poplatek_tydne])).
rmode(eq_inhabitants(+X, #['a0=_inf<x<=76801','a0=119272<x<=159134','a0=159134<x<=+inf','a0=76801<x<=99258','a0=99258<x<=119272'])).
rmode(eq_mun1(+X, #['a1=_inf<x<=16','a1=16<x<=34_5','a1=34_5<x<=57','a1=57<x<=74_5','a1=74_5<x<=+inf'])).
rmode(eq_mun2(+X, #['a2=_inf<x<=13_5','a2=13_5<x<=21_5','a2=21_5<x<=27_5','a2=27_5<x<=35_5','a2=35_5<x<=+inf'])).
rmode(eq_mun3(+X, #['a3=_inf<x<=3_5','a3=3_5<x<=4_5','a3=4_5<x<=6_5','a3=6_5<x<=9_5','a3=9_5<x<=+inf'])).
rmode(eq_mun4(+X, #['a4=_inf<x<=0_5','a4=0_5<x<=1_5','a4=1_5<x<=2_5','a4=2_5<x<=3_5','a4=3_5<x<=+inf'])).
rmode(eq_operation(+X, #[prevod_na_ucet,prevod_z_uctu,vklad,vyber,vyber_kartou,none])).
rmode(eq_payments(+X, #['a15=_inf<x<=2163','a15=2163<x<=3537_5','a15=3537_5<x<=4974_5','a15=4974_5<x<=6717','a15=6717<x<=+inf'])).
rmode(eq_ratio(+X, #['a6=_inf<x<=49_45','a6=49_45<x<=56','a6=56<x<=62_45','a6=62_45<x<=80_25','a6=80_25<x<=+inf'])).
rmode(eq_region(+X, #[prague,central_bohemia,east_bohemia,north_bohemia,north_moravia,south_bohemia,south_moravia,west_bohemia])).
rmode(eq_symbol(+X, #[pojistne,sipo,uver,none])).
rmode(eq_trans_char(+X, #[pojistne,sankc_urok,sipo,sluzby,urok,uver,none])).
rmode(eq_trans_type(+X, #[prijem,vyber,vydaj])).
rmode(eq_unemploy95(+X, #['a8=_inf<x<=1_645','a8=1_645<x<=2_585','a8=2_585<x<=3_355','a8=3_355<x<=4_71','a8=4_71<x<=+inf'])).
rmode(eq_unemploy96(+X, #['a9=_inf<x<=2_14','a9=2_14<x<=3_24','a9=3_24<x<=4_07','a9=4_07<x<=5_505','a9=5_505<x<=+inf'])).


execute(loofl(tilde,[1])).
execute(quit).
