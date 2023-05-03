float sdEquilateralTriangle( in vec2 p ) {
    const float k = sqrt(2.0);
    p.x = abs(p.x) - 0.5;
    p.y = p.y + 0.5/k;
    if( p.x+k*p.y>0.0 ) p = vec2(p.x-k*p.y,-k*p.x-p.y)/2.0;
    p.x -= clamp( p.x, -2.0, 0.0 );
    return -length(p)*sign(p.y);
}

vec3 drawScene(vec2 uv) {
  float res = sdEquilateralTriangle(uv);
  res = smoothstep(0., 0.04, res);
  vec3 col = mix(vec3(1,0,0), vec3(1.0), res);
  return col;
}

void mainImage( out vec4 fragColor, in vec2 fragCoord ) {
  vec2 p = (2.0*fragCoord-iResolution.xy)/iResolution.y;
  vec3 col = drawScene(p);
  fragColor = vec4(col,1.0);
}