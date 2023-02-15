typedef unsigned long long int bit_t;
typedef struct {
  bit_t b0;
  bit_t b1;
  bit_t b2;
  bit_t b3;
  bit_t b4;
  bit_t b5;
  bit_t b6;
  bit_t b7;
} bits;
void s(bits in, bit_t *out0, bit_t *out1, bit_t *out2, bit_t *out3, bit_t *out4, bit_t *out5, bit_t *out6, bit_t *out7) {
  bit_t var8 = in.b7 ^ in.b4;
  bit_t var9 = var8 ^ in.b6;
  bit_t var10 = var8 & in.b6;
  bit_t var11 = var10 ^ in.b2;
  bit_t var12 = var11 & in.b2;
  bit_t var13 = var9 ^ var12;
  bit_t var14 = in.b3 ^ var10;
  bit_t var15 = var14 ^ var13;
  bit_t var16 = var15 | in.b7;
  bit_t var17 = var11 ^ var16;
  bit_t var18 = var17 | in.b0;
  bit_t var19 = var13 ^ var18;
  bit_t var20 = var8 ^ in.b0;
  bit_t var21 = var20 | in.b6;
  bit_t var22 = var20 ^ in.b2;
  bit_t var23 = var22 & var19;
  bit_t var24 = var23 ^ in.b4;
  bit_t var25 = var24 & in.b2;
  bit_t var26 = var21 ^ var25;
  bit_t var27 = var26 & in.b1;
  bit_t var28 = var19 ^ var27;
  bit_t var29 = in.b7 | var11;
  bit_t var30 = var29 ^ var9;
  bit_t var31 = var28 | in.b4;
  bit_t var32 = var31 ^ var21;
  bit_t var33 = var32 | in.b2;
  bit_t var34 = in.b3 ^ var33;
  bit_t var35 = var34 & in.b1;
  bit_t var36 = var30 ^ var35;
  bit_t var37 = var36 & var28;
  bit_t var38 = var37 ^ in.b6;
  bit_t var39 = var15 ^ in.b1;
  bit_t var40 = var39 | var32;
  bit_t var41 = var40 | in.b6;
  bit_t var42 = var38 ^ var41;
  bit_t var43 = var42 | in.b0;
  bit_t var44 = var36 ^ var43;
  bit_t var45 = var44 | in.b3;
  bit_t var46 = var28 ^ var45;
  bit_t var47 = var16 & var38;
  bit_t var48 = var47 ^ var24;
  bit_t var49 = var16 & in.b0;
  bit_t var50 = var48 ^ var49;
  bit_t var51 = var38 ^ var48;
  bit_t var52 = var51 & var18;
  bit_t var53 = var49 ^ in.b2;
  bit_t var54 = var53 | var50;
  bit_t var55 = var54 | in.b3;
  bit_t var56 = var52 ^ var55;
  bit_t var57 = var56 | in.b1;
  bit_t var58 = var50 ^ var57;
  bit_t var59 = var45 & var34;
  bit_t var60 = var59 ^ var18;
  bit_t var61 = var22 | var15;
  bit_t var62 = var61 ^ var9;
  bit_t var63 = var62 & in.b7;
  bit_t var64 = var60 ^ var63;
  bit_t var65 = var17 & var46;
  bit_t var66 = var65 ^ var50;
  bit_t var67 = var46 | in.b4;
  bit_t var68 = var66 ^ var67;
  bit_t var69 = var68 | in.b1;
  bit_t var70 = var64 ^ var69;
  bit_t var71 = var70 | in.b6;
  bit_t var72 = var58 ^ var71;
  bit_t var73 = var72 | in.b5;
  *out2 = var46 ^ var73;
  bit_t var75 = var44 ^ var42;
  bit_t var76 = var75 ^ var32;
  bit_t var77 = var67 ^ *out2;
  bit_t var78 = var77 & var61;
  bit_t var79 = var78 & in.b0;
  bit_t var80 = var76 ^ var79;
  bit_t var81 = var45 ^ var17;
  bit_t var82 = var81 & var55;
  bit_t var83 = var71 | in.b7;
  bit_t var84 = var82 ^ var83;
  bit_t var85 = var84 | in.b5;
  bit_t var86 = var80 ^ var85;
  bit_t var87 = var39 ^ var72;
  bit_t var88 = var87 ^ var81;
  bit_t var89 = var51 | in.b7;
  bit_t var90 = var88 ^ var89;
  bit_t var91 = var59 ^ var16;
  bit_t var92 = var91 ^ var30;
  bit_t var93 = var92 ^ var56;
  bit_t var94 = var93 ^ var66;
  bit_t var95 = var94 & in.b0;
  bit_t var96 = var92 ^ var95;
  bit_t var97 = var96 | in.b5;
  bit_t var98 = var90 ^ var97;
  bit_t var99 = var98 | in.b4;
  bit_t var100 = var86 ^ var99;
  bit_t var101 = var18 & var94;
  bit_t var102 = var101 ^ var12;
  bit_t var103 = ~var92;
  bit_t var104 = var79 | var70;
  bit_t var105 = var104 ^ var90;
  bit_t var106 = var105 | in.b6;
  bit_t var107 = var103 ^ var106;
  bit_t var108 = var107 & in.b5;
  bit_t var109 = var102 ^ var108;
  bit_t var110 = var53 & var104;
  bit_t var111 = var110 ^ in.b5;
  bit_t var112 = var54 ^ in.b5;
  bit_t var113 = var112 & var16;
  bit_t var114 = var113 & in.b0;
  bit_t var115 = var111 ^ var114;
  bit_t var116 = var93 | var115;
  bit_t var117 = var116 ^ var103;
  bit_t var118 = var33 & in.b2;
  bit_t var119 = var117 ^ var118;
  bit_t var120 = var119 & in.b6;
  bit_t var121 = var115 ^ var120;
  bit_t var122 = var121 & in.b4;
  bit_t var123 = var109 ^ var122;
  bit_t var124 = var123 | in.b1;
  *out7 = var100 ^ var124;
  bit_t var126 = in.b5 & var25;
  bit_t var127 = var126 ^ var91;
  bit_t var128 = var127 & in.b6;
  bit_t var129 = var82 ^ var128;
  bit_t var130 = var84 | var98;
  bit_t var131 = var130 ^ var109;
  bit_t var132 = ~var38;
  bit_t var133 = var132 | in.b4;
  bit_t var134 = var131 ^ var133;
  bit_t var135 = var134 | in.b1;
  bit_t var136 = var129 ^ var135;
  bit_t var137 = var111 | var66;
  bit_t var138 = var137 ^ var21;
  bit_t var139 = var109 | var94;
  bit_t var140 = var139 ^ var48;
  bit_t var141 = var140 & in.b1;
  bit_t var142 = var138 ^ var141;
  bit_t var143 = var90 ^ var27;
  bit_t var144 = var143 ^ var142;
  bit_t var145 = var144 & in.b2;
  bit_t var146 = *out7 ^ var145;
  bit_t var147 = var146 & in.b3;
  bit_t var148 = var142 ^ var147;
  bit_t var149 = var148 & in.b7;
  bit_t var150 = var136 ^ var149;
  bit_t var151 = var54 ^ var44;
  bit_t var152 = var151 ^ var146;
  bit_t var153 = var87 | var64;
  bit_t var154 = var153 ^ var128;
  bit_t var155 = var154 | in.b1;
  bit_t var156 = var152 ^ var155;
  bit_t var157 = var35 & var53;
  bit_t var158 = var157 ^ var77;
  bit_t var159 = var158 & in.b5;
  bit_t var160 = var156 ^ var159;
  bit_t var161 = ~var106;
  bit_t var162 = var158 | var82;
  bit_t var163 = var162 ^ var144;
  bit_t var164 = var163 | in.b2;
  bit_t var165 = var161 ^ var164;
  bit_t var166 = var68 | var93;
  bit_t var167 = var166 ^ var55;
  bit_t var168 = var10 | in.b5;
  bit_t var169 = var167 ^ var168;
  bit_t var170 = var169 & in.b3;
  bit_t var171 = var165 ^ var170;
  bit_t var172 = var171 | in.b7;
  bit_t var173 = var160 ^ var172;
  bit_t var174 = var173 & in.b0;
  *out0 = var150 ^ var174;
  bit_t var176 = var26 | *out0;
  bit_t var177 = var176 ^ var158;
  bit_t var178 = var44 ^ var68;
  bit_t var179 = var178 ^ var123;
  bit_t var180 = var179 & in.b0;
  bit_t var181 = var177 ^ var180;
  bit_t var182 = var137 | var42;
  bit_t var183 = var182 ^ var51;
  bit_t var184 = var183 & in.b3;
  bit_t var185 = var181 ^ var184;
  bit_t var186 = var14 ^ var75;
  bit_t var187 = var186 ^ var88;
  bit_t var188 = in.b7 ^ var105;
  bit_t var189 = var188 ^ var39;
  bit_t var190 = var88 | var176;
  bit_t var191 = var190 ^ var181;
  bit_t var192 = var191 & in.b0;
  bit_t var193 = var189 ^ var192;
  bit_t var194 = var193 | in.b4;
  bit_t var195 = var187 ^ var194;
  bit_t var196 = var195 & in.b7;
  bit_t var197 = var185 ^ var196;
  bit_t var198 = var34 ^ var173;
  bit_t var199 = var198 ^ var192;
  bit_t var200 = var12 | var198;
  bit_t var201 = var200 ^ var38;
  bit_t var202 = var201 & in.b6;
  bit_t var203 = var102 ^ var202;
  bit_t var204 = var203 & in.b2;
  bit_t var205 = var199 ^ var204;
  bit_t var206 = var25 | var76;
  bit_t var207 = var206 ^ var193;
  bit_t var208 = ~var204;
  bit_t var209 = var208 & in.b6;
  bit_t var210 = var207 ^ var209;
  bit_t var211 = var50 ^ var138;
  bit_t var212 = var211 ^ var188;
  bit_t var213 = var52 & in.b4;
  bit_t var214 = var212 ^ var213;
  bit_t var215 = var214 & in.b1;
  bit_t var216 = var210 ^ var215;
  bit_t var217 = var216 & in.b3;
  bit_t var218 = var205 ^ var217;
  bit_t var219 = var218 & in.b5;
  *out5 = var197 ^ var219;
  bit_t var221 = var61 & *out0;
  bit_t var222 = var221 ^ var56;
  bit_t var223 = ~var164;
  bit_t var224 = var223 | in.b0;
  bit_t var225 = var222 ^ var224;
  bit_t var226 = var146 ^ var179;
  bit_t var227 = var226 ^ var221;
  bit_t var228 = var164 & in.b4;
  bit_t var229 = var227 ^ var228;
  bit_t var230 = var229 & in.b3;
  bit_t var231 = var225 ^ var230;
  bit_t var232 = var198 ^ var120;
  bit_t var233 = var232 ^ var203;
  bit_t var234 = var105 ^ var40;
  bit_t var235 = var234 ^ var226;
  bit_t var236 = var235 & in.b2;
  bit_t var237 = var233 ^ var236;
  bit_t var238 = var166 & var81;
  bit_t var239 = var238 ^ var40;
  bit_t var240 = var239 | in.b0;
  bit_t var241 = var237 ^ var240;
  bit_t var242 = var241 | in.b1;
  bit_t var243 = var231 ^ var242;
  bit_t var244 = var93 ^ var166;
  bit_t var245 = var244 ^ var202;
  bit_t var246 = var214 & var197;
  bit_t var247 = var246 ^ var234;
  bit_t var248 = var247 & in.b0;
  bit_t var249 = var245 ^ var248;
  bit_t var250 = var156 ^ in.b3;
  bit_t var251 = var250 ^ var203;
  bit_t var252 = var251 | in.b7;
  bit_t var253 = var246 ^ var252;
  bit_t var254 = var253 & in.b1;
  bit_t var255 = var249 ^ var254;
  bit_t var256 = var134 | var63;
  bit_t var257 = var256 & var173;
  bit_t var258 = var157 | var169;
  bit_t var259 = var258 ^ var117;
  bit_t var260 = var159 | in.b3;
  bit_t var261 = var259 ^ var260;
  bit_t var262 = var261 & in.b4;
  bit_t var263 = var257 ^ var262;
  bit_t var264 = var263 & in.b2;
  bit_t var265 = var255 ^ var264;
  bit_t var266 = var265 & in.b5;
  *out3 = var243 ^ var266;
  bit_t var268 = var245 | *out2;
  bit_t var269 = var268 ^ var60;
  bit_t var270 = var36 & var48;
  bit_t var271 = var270 ^ var205;
  bit_t var272 = var271 & in.b0;
  bit_t var273 = var269 ^ var272;
  bit_t var274 = var251 | var102;
  bit_t var275 = var274 ^ var49;
  bit_t var276 = var275 & in.b6;
  bit_t var277 = var243 ^ var276;
  bit_t var278 = var277 | in.b4;
  bit_t var279 = var273 ^ var278;
  bit_t var280 = var18 & var8;
  bit_t var281 = var280 ^ var226;
  bit_t var282 = var203 | var261;
  bit_t var283 = var282 ^ var40;
  bit_t var284 = var283 | in.b0;
  bit_t var285 = var245 ^ var284;
  bit_t var286 = var285 | in.b4;
  bit_t var287 = var281 ^ var286;
  bit_t var288 = var287 & in.b3;
  bit_t var289 = var279 ^ var288;
  bit_t var290 = var222 | var36;
  bit_t var291 = var290 ^ var24;
  bit_t var292 = var92 & var70;
  bit_t var293 = var292 ^ var181;
  bit_t var294 = ~var252;
  bit_t var295 = var294 & in.b6;
  bit_t var296 = var293 ^ var295;
  bit_t var297 = var296 & in.b4;
  bit_t var298 = var291 ^ var297;
  bit_t var299 = var266 ^ var57;
  bit_t var300 = var299 & var293;
  bit_t var301 = var239 & var241;
  bit_t var302 = var301 ^ var66;
  bit_t var303 = ~var205;
  bit_t var304 = var303 | in.b6;
  bit_t var305 = var302 ^ var304;
  bit_t var306 = var305 & in.b3;
  bit_t var307 = var300 ^ var306;
  bit_t var308 = var307 & in.b2;
  bit_t var309 = var298 ^ var308;
  bit_t var310 = var309 & in.b5;
  *out4 = var289 ^ var310;
  bit_t var312 = var64 | var199;
  bit_t var313 = var312 ^ var139;
  bit_t var314 = var226 | var235;
  bit_t var315 = var314 ^ var65;
  bit_t var316 = var315 & in.b0;
  bit_t var317 = var313 ^ var316;
  bit_t var318 = var19 ^ var263;
  bit_t var319 = var318 ^ var161;
  bit_t var320 = var188 & in.b2;
  bit_t var321 = var319 ^ var320;
  bit_t var322 = var321 & in.b3;
  bit_t var323 = var317 ^ var322;
  bit_t var324 = *out2 ^ var315;
  bit_t var325 = var324 | var309;
  bit_t var326 = var205 & in.b0;
  bit_t var327 = var325 ^ var326;
  bit_t var328 = var314 ^ var151;
  bit_t var329 = var328 & var8;
  bit_t var330 = var329 | in.b2;
  bit_t var331 = var327 ^ var330;
  bit_t var332 = var331 & in.b4;
  bit_t var333 = var323 ^ var332;
  bit_t var334 = var11 | var73;
  bit_t var335 = var334 ^ var31;
  bit_t var336 = var307 ^ var82;
  bit_t var337 = var336 | var60;
  bit_t var338 = var337 & in.b7;
  bit_t var339 = var81 ^ var338;
  bit_t var340 = var339 | in.b2;
  bit_t var341 = var335 ^ var340;
  bit_t var342 = var131 & var35;
  bit_t var343 = var342 ^ var271;
  bit_t var344 = var343 | in.b6;
  bit_t var345 = var55 ^ var344;
  bit_t var346 = ~var135;
  bit_t var347 = var240 ^ var309;
  bit_t var348 = var347 | var192;
  bit_t var349 = var348 & in.b2;
  bit_t var350 = var346 ^ var349;
  bit_t var351 = var350 & in.b3;
  bit_t var352 = var345 ^ var351;
  bit_t var353 = var352 & in.b4;
  bit_t var354 = var341 ^ var353;
  bit_t var355 = var354 | in.b5;
  *out1 = var333 ^ var355;
  bit_t var357 = var200 & var28;
  bit_t var358 = var357 | var231;
  bit_t var359 = var166 & in.b6;
  bit_t var360 = var358 ^ var359;
  bit_t var361 = var323 & var225;
  bit_t var362 = var361 ^ var331;
  bit_t var363 = var319 ^ var362;
  bit_t var364 = var363 ^ var117;
  bit_t var365 = var364 & in.b0;
  bit_t var366 = var362 ^ var365;
  bit_t var367 = var366 & in.b7;
  bit_t var368 = var360 ^ var367;
  bit_t var369 = var151 | var269;
  bit_t var370 = var369 ^ var221;
  bit_t var371 = var370 & in.b0;
  bit_t var372 = var184 ^ var371;
  bit_t var373 = var63 ^ var257;
  bit_t var374 = var373 | var52;
  bit_t var375 = var374 & in.b7;
  bit_t var376 = var372 ^ var375;
  bit_t var377 = var376 | in.b5;
  bit_t var378 = var368 ^ var377;
  bit_t var379 = var227 & var200;
  bit_t var380 = var379 ^ in.b3;
  bit_t var381 = var39 & var187;
  bit_t var382 = var381 | var321;
  bit_t var383 = var87 & in.b4;
  bit_t var384 = var382 ^ var383;
  bit_t var385 = var384 & in.b0;
  bit_t var386 = var380 ^ var385;
  bit_t var387 = var376 & var193;
  bit_t var388 = var387 ^ var372;
  bit_t var389 = var83 ^ var93;
  bit_t var390 = var389 & var169;
  bit_t var391 = var390 & in.b4;
  bit_t var392 = var210 ^ var391;
  bit_t var393 = var392 | in.b2;
  bit_t var394 = var388 ^ var393;
  bit_t var395 = var394 & in.b7;
  bit_t var396 = var386 ^ var395;
  bit_t var397 = var396 & in.b1;
  *out6 = var378 ^ var397;
}
