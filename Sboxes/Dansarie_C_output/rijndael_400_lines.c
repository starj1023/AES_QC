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
  bit_t var8 = (in.b7 & in.b5) | (~in.b7 & ~in.b5);
  bit_t var9 = (var8 & in.b2) | (~var8 & ~in.b2);
  bit_t var10 = var9 & in.b5;
  bit_t var11 = var10 ^ var8;
  bit_t var12 = var11 | in.b4;
  bit_t var13 = var9 ^ var12;
  bit_t var14 = (var9 & in.b4) | (~var9 & ~in.b4);
  bit_t var15 = var14 ^ var12;
  bit_t var16 = var11 | in.b7;
  bit_t var17 = var15 ^ var16;
  bit_t var18 = var17 & in.b3;
  bit_t var19 = var13 ^ var18;
  bit_t var20 = (in.b7 & var18) | (~in.b7 & ~var18);
  bit_t var21 = var20 & var14;
  bit_t var22 = ~in.b3;
  bit_t var23 = var22 & in.b2;
  bit_t var24 = var21 ^ var23;
  bit_t var25 = var24 & in.b2;
  bit_t var26 = (var25 & var18) | (~var25 & ~var18);
  bit_t var27 = var26 & in.b4;
  bit_t var28 = var24 ^ var27;
  bit_t var29 = var28 & in.b6;
  bit_t var30 = var19 ^ var29;
  bit_t var31 = in.b7 & var19;
  bit_t var32 = (var31 & in.b1) | (~var31 & ~in.b1);
  bit_t var33 = var14 | in.b3;
  bit_t var34 = var32 ^ var33;
  bit_t var35 = in.b5 & var30;
  bit_t var36 = (var35 & var26) | (~var35 & ~var26);
  bit_t var37 = var36 & in.b2;
  bit_t var38 = var34 ^ var37;
  bit_t var39 = (in.b1 & var17) | (~in.b1 & ~var17);
  bit_t var40 = (var39 & var32) | (~var39 & ~var32);
  bit_t var41 = var40 | in.b5;
  bit_t var42 = var28 ^ var41;
  bit_t var43 = var42 & in.b6;
  bit_t var44 = var38 ^ var43;
  bit_t var45 = var44 | in.b0;
  bit_t var46 = var30 ^ var45;
  bit_t var47 = var34 ^ in.b2;
  bit_t var48 = var47 & var28;
  bit_t var49 = (var47 & var44) | (~var47 & ~var44);
  bit_t var50 = var49 & var34;
  bit_t var51 = var50 | in.b7;
  bit_t var52 = var48 ^ var51;
  bit_t var53 = var47 & var52;
  bit_t var54 = (var53 & var46) | (~var53 & ~var46);
  bit_t var55 = (var14 & var49) | (~var14 & ~var49);
  bit_t var56 = (var55 & in.b5) | (~var55 & ~in.b5);
  bit_t var57 = var56 & in.b3;
  bit_t var58 = var54 ^ var57;
  bit_t var59 = var58 | in.b0;
  bit_t var60 = var52 ^ var59;
  bit_t var61 = (var16 & var37) | (~var16 & ~var37);
  bit_t var62 = (var61 & var24) | (~var61 & ~var24);
  bit_t var63 = var62 & in.b3;
  bit_t var64 = var20 ^ var63;
  bit_t var65 = var22 & var20;
  bit_t var66 = var65 ^ var12;
  bit_t var67 = var28 & var53;
  bit_t var68 = var67 ^ var10;
  bit_t var69 = var68 & in.b2;
  bit_t var70 = var66 ^ var69;
  bit_t var71 = var70 & in.b0;
  bit_t var72 = var64 ^ var71;
  bit_t var73 = var72 & in.b6;
  bit_t var74 = var60 ^ var73;
  bit_t var75 = var74 & in.b1;
  *out0 = var46 ^ var75;
  bit_t var77 = var41 & var38;
  bit_t var78 = var77 ^ var8;
  bit_t var79 = (var17 & var58) | (~var17 & ~var58);
  bit_t var80 = var79 & var41;
  bit_t var81 = var80 | in.b6;
  bit_t var82 = var78 ^ var81;
  bit_t var83 = (var82 & var74) | (~var82 & ~var74);
  bit_t var84 = var83 & var36;
  bit_t var85 = (var57 & var74) | (~var57 & ~var74);
  bit_t var86 = (var85 & var70) | (~var85 & ~var70);
  bit_t var87 = var86 & in.b5;
  bit_t var88 = var84 ^ var87;
  bit_t var89 = var88 | in.b0;
  bit_t var90 = var82 ^ var89;
  bit_t var91 = var66 & var11;
  bit_t var92 = var91 ^ var44;
  bit_t var93 = (var18 & var83) | (~var18 & ~var83);
  bit_t var94 = var93 ^ var33;
  bit_t var95 = var94 & in.b0;
  bit_t var96 = var92 ^ var95;
  bit_t var97 = (var69 & var74) | (~var69 & ~var74);
  bit_t var98 = (var97 & var84) | (~var97 & ~var84);
  bit_t var99 = var98 & in.b6;
  bit_t var100 = var96 ^ var99;
  bit_t var101 = var100 & in.b4;
  bit_t var102 = var90 ^ var101;
  bit_t var103 = var56 & var10;
  bit_t var104 = var103 ^ var19;
  bit_t var105 = var104 & in.b6;
  bit_t var106 = var68 ^ var105;
  bit_t var107 = (var30 & var17) | (~var30 & ~var17);
  bit_t var108 = var107 ^ var98;
  bit_t var109 = var107 & var45;
  bit_t var110 = (var109 & var80) | (~var109 & ~var80);
  bit_t var111 = var110 & in.b2;
  bit_t var112 = var108 ^ var111;
  bit_t var113 = var112 | in.b5;
  bit_t var114 = var106 ^ var113;
  bit_t var115 = (var69 & var15) | (~var69 & ~var15);
  bit_t var116 = (var115 & var22) | (~var115 & ~var22);
  bit_t var117 = var116 | in.b5;
  bit_t var118 = var101 ^ var117;
  bit_t var119 = (var96 & var18) | (~var96 & ~var18);
  bit_t var120 = (var119 & var114) | (~var119 & ~var114);
  bit_t var121 = (var28 & var100) | (~var28 & ~var100);
  bit_t var122 = (var121 & var116) | (~var121 & ~var116);
  bit_t var123 = var122 | in.b2;
  bit_t var124 = var120 ^ var123;
  bit_t var125 = var124 | in.b4;
  bit_t var126 = var118 ^ var125;
  bit_t var127 = var126 & in.b0;
  bit_t var128 = var114 ^ var127;
  bit_t var129 = var128 & in.b1;
  *out1 = var102 ^ var129;
  bit_t var131 = var32 & var121;
  bit_t var132 = var131 ^ var21;
  bit_t var133 = var26 & var120;
  bit_t var134 = (var133 & var107) | (~var133 & ~var107);
  bit_t var135 = var134 & in.b1;
  bit_t var136 = var132 ^ var135;
  bit_t var137 = (var103 & var88) | (~var103 & ~var88);
  bit_t var138 = var137 ^ var115;
  bit_t var139 = var138 & in.b1;
  bit_t var140 = var122 ^ var139;
  bit_t var141 = var140 | in.b6;
  bit_t var142 = var136 ^ var141;
  bit_t var143 = var133 ^ var70;
  bit_t var144 = var143 & var49;
  bit_t var145 = var78 ^ var52;
  bit_t var146 = var145 & var73;
  bit_t var147 = var146 | in.b7;
  bit_t var148 = var133 ^ var147;
  bit_t var149 = var148 | in.b3;
  bit_t var150 = var144 ^ var149;
  bit_t var151 = var150 | in.b4;
  bit_t var152 = var142 ^ var151;
  bit_t var153 = (var70 & var149) | (~var70 & ~var149);
  bit_t var154 = (var153 & var58) | (~var153 & ~var58);
  bit_t var155 = ~var73;
  bit_t var156 = var155 & in.b4;
  bit_t var157 = var154 ^ var156;
  bit_t var158 = (in.b4 & var88) | (~in.b4 & ~var88);
  bit_t var159 = (var158 & var80) | (~var158 & ~var80);
  bit_t var160 = var159 & var100;
  bit_t var161 = var160 ^ var118;
  bit_t var162 = var161 & in.b1;
  bit_t var163 = var159 ^ var162;
  bit_t var164 = var163 | in.b5;
  bit_t var165 = var157 ^ var164;
  bit_t var166 = (var122 & var93) | (~var122 & ~var93);
  bit_t var167 = var166 & var78;
  bit_t var168 = var167 | in.b5;
  bit_t var169 = var82 ^ var168;
  bit_t var170 = var155 & var138;
  bit_t var171 = var170 ^ var64;
  bit_t var172 = var62 & in.b7;
  bit_t var173 = var171 ^ var172;
  bit_t var174 = var173 & in.b1;
  bit_t var175 = var169 ^ var174;
  bit_t var176 = var175 & in.b2;
  bit_t var177 = var165 ^ var176;
  bit_t var178 = var177 & in.b0;
  *out5 = var152 ^ var178;
  bit_t var180 = var62 ^ var153;
  bit_t var181 = var180 & var41;
  bit_t var182 = var35 & in.b7;
  bit_t var183 = var181 ^ var182;
  bit_t var184 = (var53 & var133) | (~var53 & ~var133);
  bit_t var185 = (var184 & var183) | (~var184 & ~var183);
  bit_t var186 = var151 & var50;
  bit_t var187 = (var186 & var183) | (~var186 & ~var183);
  bit_t var188 = var187 & in.b2;
  bit_t var189 = var185 ^ var188;
  bit_t var190 = var189 & in.b1;
  bit_t var191 = var183 ^ var190;
  bit_t var192 = var79 & var119;
  bit_t var193 = (var192 & var147) | (~var192 & ~var147);
  bit_t var194 = var147 & var125;
  bit_t var195 = (var194 & var33) | (~var194 & ~var33);
  bit_t var196 = var195 & in.b1;
  bit_t var197 = var193 ^ var196;
  bit_t var198 = (var103 & var143) | (~var103 & ~var143);
  bit_t var199 = (var198 & var111) | (~var198 & ~var111);
  bit_t var200 = var199 & in.b5;
  bit_t var201 = var197 ^ var200;
  bit_t var202 = var201 & in.b0;
  bit_t var203 = var191 ^ var202;
  bit_t var204 = var102 & var46;
  bit_t var205 = var204 ^ var201;
  bit_t var206 = (var193 & var185) | (~var193 & ~var185);
  bit_t var207 = (var206 & var164) | (~var206 & ~var164);
  bit_t var208 = var207 & in.b0;
  bit_t var209 = var205 ^ var208;
  bit_t var210 = (var50 & var102) | (~var50 & ~var102);
  bit_t var211 = var210 ^ var152;
  bit_t var212 = var211 & in.b0;
  bit_t var213 = var193 ^ var212;
  bit_t var214 = var213 & in.b6;
  bit_t var215 = var209 ^ var214;
  bit_t var216 = ~var206;
  bit_t var217 = (var164 & var107) | (~var164 & ~var107);
  bit_t var218 = var217 ^ var215;
  bit_t var219 = var218 | in.b0;
  bit_t var220 = var216 ^ var219;
  bit_t var221 = *out5 & var89;
  bit_t var222 = var221 ^ var86;
  bit_t var223 = var222 & in.b4;
  bit_t var224 = var220 ^ var223;
  bit_t var225 = var224 & in.b7;
  bit_t var226 = var215 ^ var225;
  bit_t var227 = var226 & in.b3;
  *out2 = var203 ^ var227;
  bit_t var229 = (var105 & var50) | (~var105 & ~var50);
  bit_t var230 = (var229 & var182) | (~var229 & ~var182);
  bit_t var231 = (var120 & var192) | (~var120 & ~var192);
  bit_t var232 = (var231 & var171) | (~var231 & ~var171);
  bit_t var233 = var232 & in.b0;
  bit_t var234 = var230 ^ var233;
  bit_t var235 = var66 & var158;
  bit_t var236 = var235 ^ var119;
  bit_t var237 = var236 | in.b0;
  bit_t var238 = var105 ^ var237;
  bit_t var239 = var238 | in.b4;
  bit_t var240 = var234 ^ var239;
  bit_t var241 = (var224 & var132) | (~var224 & ~var132);
  bit_t var242 = var241 & var16;
  bit_t var243 = ~var57;
  bit_t var244 = var243 | in.b4;
  bit_t var245 = var242 ^ var244;
  bit_t var246 = var238 & var219;
  bit_t var247 = var246 ^ var217;
  bit_t var248 = var247 | in.b2;
  bit_t var249 = var245 ^ var248;
  bit_t var250 = var249 & in.b1;
  bit_t var251 = var240 ^ var250;
  bit_t var252 = var42 & var45;
  bit_t var253 = var252 ^ var75;
  bit_t var254 = var253 | in.b3;
  bit_t var255 = var104 ^ var254;
  bit_t var256 = (var216 & var247) | (~var216 & ~var247);
  bit_t var257 = var256 ^ var199;
  bit_t var258 = var257 & in.b4;
  bit_t var259 = var92 ^ var258;
  bit_t var260 = var259 & in.b2;
  bit_t var261 = var255 ^ var260;
  bit_t var262 = (var13 & var80) | (~var13 & ~var80);
  bit_t var263 = var262 ^ var164;
  bit_t var264 = ~var24;
  bit_t var265 = (var247 & var240) | (~var247 & ~var240);
  bit_t var266 = (var265 & var133) | (~var265 & ~var133);
  bit_t var267 = var266 & in.b0;
  bit_t var268 = var264 ^ var267;
  bit_t var269 = var268 | in.b1;
  bit_t var270 = var263 ^ var269;
  bit_t var271 = var270 & in.b7;
  bit_t var272 = var261 ^ var271;
  bit_t var273 = var272 | in.b6;
  *out3 = var251 ^ var273;
  bit_t var275 = (var102 & var163) | (~var102 & ~var163);
  bit_t var276 = (var275 & var249) | (~var275 & ~var249);
  bit_t var277 = (var67 & var9) | (~var67 & ~var9);
  bit_t var278 = var277 ^ var224;
  bit_t var279 = var278 & in.b1;
  bit_t var280 = var276 ^ var279;
  bit_t var281 = var154 & var88;
  bit_t var282 = (var281 & var143) | (~var281 & ~var143);
  bit_t var283 = var282 | in.b3;
  bit_t var284 = var280 ^ var283;
  bit_t var285 = (var185 & var276) | (~var185 & ~var276);
  bit_t var286 = var285 & var239;
  bit_t var287 = (var151 & var258) | (~var151 & ~var258);
  bit_t var288 = var287 ^ var224;
  bit_t var289 = *out1 & var119;
  bit_t var290 = var289 ^ var257;
  bit_t var291 = var290 & in.b1;
  bit_t var292 = var288 ^ var291;
  bit_t var293 = var292 & in.b3;
  bit_t var294 = var286 ^ var293;
  bit_t var295 = var294 | in.b5;
  bit_t var296 = var284 ^ var295;
  bit_t var297 = (var241 & var247) | (~var241 & ~var247);
  bit_t var298 = var297 ^ var117;
  bit_t var299 = var252 | in.b2;
  bit_t var300 = var298 ^ var299;
  bit_t var301 = var110 | in.b6;
  bit_t var302 = var260 ^ var301;
  bit_t var303 = var302 | in.b4;
  bit_t var304 = var300 ^ var303;
  bit_t var305 = var132 & var122;
  bit_t var306 = (var305 & in.b2) | (~var305 & ~in.b2);
  bit_t var307 = var34 & var226;
  bit_t var308 = (var307 & in.b0) | (~var307 & ~in.b0);
  bit_t var309 = var308 & in.b1;
  bit_t var310 = var306 ^ var309;
  bit_t var311 = var55 & var107;
  bit_t var312 = var311 ^ var78;
  bit_t var313 = ~var105;
  bit_t var314 = var313 | in.b1;
  bit_t var315 = var312 ^ var314;
  bit_t var316 = var315 & in.b4;
  bit_t var317 = var310 ^ var316;
  bit_t var318 = var317 & in.b7;
  bit_t var319 = var304 ^ var318;
  bit_t var320 = var319 | in.b0;
  *out6 = var296 ^ var320;
  bit_t var322 = (var198 & var87) | (~var198 & ~var87);
  bit_t var323 = var322 & var49;
  bit_t var324 = (var109 & var256) | (~var109 & ~var256);
  bit_t var325 = var324 ^ var189;
  bit_t var326 = var255 & var187;
  bit_t var327 = (var326 & var176) | (~var326 & ~var176);
  bit_t var328 = var327 & in.b1;
  bit_t var329 = var325 ^ var328;
  bit_t var330 = var329 | in.b0;
  bit_t var331 = var323 ^ var330;
  bit_t var332 = (var284 & var265) | (~var284 & ~var265);
  bit_t var333 = var332 ^ var54;
  bit_t var334 = ~var330;
  bit_t var335 = var334 & in.b6;
  bit_t var336 = var333 ^ var335;
  bit_t var337 = var90 ^ var325;
  bit_t var338 = var337 & var312;
  bit_t var339 = var338 & in.b7;
  bit_t var340 = var336 ^ var339;
  bit_t var341 = var340 | in.b3;
  bit_t var342 = var331 ^ var341;
  bit_t var343 = var119 & var173;
  bit_t var344 = (var343 & var126) | (~var343 & ~var126);
  bit_t var345 = var102 & in.b1;
  bit_t var346 = var344 ^ var345;
  bit_t var347 = (*out6 & var204) | (~*out6 & ~var204);
  bit_t var348 = var347 & var32;
  bit_t var349 = var348 | in.b7;
  bit_t var350 = var346 ^ var349;
  bit_t var351 = var350 & var199;
  bit_t var352 = var351 ^ var294;
  bit_t var353 = var352 | in.b4;
  bit_t var354 = var161 ^ var353;
  bit_t var355 = (var157 & var180) | (~var157 & ~var180);
  bit_t var356 = var355 ^ var271;
  bit_t var357 = var342 | in.b4;
  bit_t var358 = var356 ^ var357;
  bit_t var359 = var358 | in.b0;
  bit_t var360 = var354 ^ var359;
  bit_t var361 = var360 & in.b6;
  bit_t var362 = var350 ^ var361;
  bit_t var363 = var362 | in.b2;
  *out4 = var342 ^ var363;
  bit_t var365 = (var359 & var122) | (~var359 & ~var122);
  bit_t var366 = (var365 & *out1) | (~var365 & ~*out1);
  bit_t var367 = var366 | in.b4;
  bit_t var368 = var136 ^ var367;
  bit_t var369 = (var181 & var339) | (~var181 & ~var339);
  bit_t var370 = var369 ^ var150;
  bit_t var371 = var370 | in.b1;
  bit_t var372 = var368 ^ var371;
  bit_t var373 = (var224 & var184) | (~var224 & ~var184);
  bit_t var374 = var373 ^ var342;
  bit_t var375 = (var284 & var184) | (~var284 & ~var184);
  bit_t var376 = var375 ^ var100;
  bit_t var377 = (var26 & var351) | (~var26 & ~var351);
  bit_t var378 = var377 ^ var308;
  bit_t var379 = var378 & in.b1;
  bit_t var380 = var376 ^ var379;
  bit_t var381 = var380 | in.b7;
  bit_t var382 = var374 ^ var381;
  bit_t var383 = var382 & in.b0;
  bit_t var384 = var372 ^ var383;
  bit_t var385 = (var282 & var292) | (~var282 & ~var292);
  bit_t var386 = var385 & var268;
  bit_t var387 = var199 & var372;
  bit_t var388 = (var387 & in.b0) | (~var387 & ~in.b0);
  bit_t var389 = var204 & in.b7;
  bit_t var390 = var388 ^ var389;
  bit_t var391 = var390 & in.b4;
  bit_t var392 = var386 ^ var391;
  bit_t var393 = var276 ^ var304;
  bit_t var394 = var393 & var36;
  bit_t var395 = var394 & in.b0;
  bit_t var396 = var204 ^ var395;
  bit_t var397 = (var202 & var333) | (~var202 & ~var333);
  bit_t var398 = var397 ^ var58;
  bit_t var399 = ~var290;
  bit_t var400 = var399 & in.b2;
  bit_t var401 = var398 ^ var400;
  bit_t var402 = var401 | in.b4;
  bit_t var403 = var396 ^ var402;
  bit_t var404 = var403 | in.b6;
  bit_t var405 = var392 ^ var404;
  bit_t var406 = var405 & in.b5;
  *out7 = var384 ^ var406;
}
