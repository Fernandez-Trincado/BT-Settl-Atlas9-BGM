awk 'NR<3{print}' m05.dat > a_m05.dat
awk 'NR>2{print}' m05.dat >> temp_m05.dat
sort -k1  temp_m05.dat >> a_m05.dat
mv a_m05.dat m05.dat
rm  No_inter_m05.dat temp_m05.dat
awk 'NR<3{print}' m10.dat > a_m10.dat
awk 'NR>2{print}' m10.dat >> temp_m10.dat
sort -k1  temp_m10.dat >> a_m10.dat
mv a_m10.dat m10.dat
rm  No_inter_m10.dat temp_m10.dat
awk 'NR<3{print}' m15.dat > a_m15.dat
awk 'NR>2{print}' m15.dat >> temp_m15.dat
sort -k1  temp_m15.dat >> a_m15.dat
mv a_m15.dat m15.dat
rm  No_inter_m15.dat temp_m15.dat
awk 'NR<3{print}' m20.dat > a_m20.dat
awk 'NR>2{print}' m20.dat >> temp_m20.dat
sort -k1  temp_m20.dat >> a_m20.dat
mv a_m20.dat m20.dat
rm  No_inter_m20.dat temp_m20.dat
awk 'NR<3{print}' m25.dat > a_m25.dat
awk 'NR>2{print}' m25.dat >> temp_m25.dat
sort -k1  temp_m25.dat >> a_m25.dat
mv a_m25.dat m25.dat
rm  No_inter_m25.dat temp_m25.dat
awk 'NR<3{print}' m40.dat > a_m40.dat
awk 'NR>2{print}' m40.dat >> temp_m40.dat
sort -k1  temp_m40.dat >> a_m40.dat
mv a_m40.dat m40.dat
rm  No_inter_m40.dat temp_m40.dat
awk 'NR<3{print}' p00.dat > a_p00.dat
awk 'NR>2{print}' p00.dat >> temp_p00.dat
sort -k1  temp_p00.dat >> a_p00.dat
mv a_p00.dat p00.dat
rm  No_inter_p00.dat temp_p00.dat
awk 'NR<3{print}' p02.dat > a_p02.dat
awk 'NR>2{print}' p02.dat >> temp_p02.dat
sort -k1  temp_p02.dat >> a_p02.dat
mv a_p02.dat p02.dat
rm  No_inter_p02.dat temp_p02.dat
awk 'NR<3{print}' p05.dat > a_p05.dat
awk 'NR>2{print}' p05.dat >> temp_p05.dat
sort -k1  temp_p05.dat >> a_p05.dat
mv a_p05.dat p05.dat
rm  No_inter_p05.dat temp_p05.dat
