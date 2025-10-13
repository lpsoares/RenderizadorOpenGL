#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Demonstração de compatibilidade com ShaderToy.

Este exemplo mostra como executar shaders do ShaderToy diretamente com o RenderizadorOpenGL.
Basta copiar e colar o código de um shader do ShaderToy e ele funcionará sem modificações.
"""

import os
import sys
from renderizador import Renderizador

# Shader do ShaderToy - Plasma Globe
# Original: https://www.shadertoy.com/view/XsjXRm
SHADERTOY_CODE = """
// Plasma Globe by nimitz (twitter: @stormoid)
// https://www.shadertoy.com/view/XsjXRm
// License Creative Commons Attribution-NonCommercial-ShareAlike 3.0 Unported License
// Contact the author for other licensing options

//looks best with around 25 rays
#define NUM_RAYS 25.

#define VOLUMETRIC_STEPS 19

#define MAX_ITER 35
#define FAR 6.

#define time iTime*1.1


mat2 mm2(in float a){float c = cos(a), s = sin(a);return mat2(c,-s,s,c);}
float noise( in float x ){return textureLod(iChannel0, vec2(x*.01,1.),0.0).x;}

float hash( float n ){return fract(sin(n)*43758.5453);}

float noise(in vec3 p)
{
    vec3 ip = floor(p);
    vec3 fp = fract(p);
    fp = fp*fp*(3.0-2.0*fp);
    
    vec2 tap = (ip.xy+vec2(37.0,17.0)*ip.z) + fp.xy;
    vec2 rg = textureLod( iChannel0, (tap + 0.5)/256.0, 0.0 ).yx;
    return mix(rg.x, rg.y, fp.z);
}

mat3 m3 = mat3( 0.00,  0.80,  0.60,
               -0.80,  0.36, -0.48,
               -0.60, -0.48,  0.64 );


//See: https://www.shadertoy.com/view/XdfXRj
float flow(in vec3 p, in float t)
{
    float z=2.;
    float rz = 0.;
    vec3 bp = p;
    for (float i= 1.;i < 5.;i++ )
    {
        p += time*.1;
        rz+= (sin(noise(p+t*0.8)*6.)*0.5+0.5) /z;
        p = mix(bp,p,0.6);
        z *= 2.;
        p *= 2.01;
        p*= m3;
    }
    return rz;
}

//could be improved
float sins(in float x)
{
 	float rz = 0.;
    float z = 2.;
    for (float i= 0.;i < 3.;i++ )
    {
        rz += abs(fract(x*1.4)-0.5)/z;
        x *= 1.3;
        z *= 1.15;
        x -= time*.65*z;
    }
    return rz;
}

float segm( vec3 p, vec3 a, vec3 b)
{
    vec3 pa = p - a;
    vec3 ba = b - a;
    float h = clamp( dot(pa,ba)/dot(ba,ba), 0.0, 1.0 );
    return length( pa - ba*h )*.5;
}

vec3 path(in float i, in float d)
{
    vec3 en = vec3(0.,0.,1.);
    float sns2 = sins(d+i*0.5)*0.22;
    float sns = sins(d+i*.6)*0.21;
    en.xz *= mm2((hash(i*10.569)-.5)*6.2+sns2);
    en.xy *= mm2((hash(i*4.732)-.5)*6.2+sns);
    return en;
}

vec2 map(vec3 p, float i)
{
    float lp = length(p);
    vec3 bg = vec3(0.);   
    vec3 en = path(i,lp);
    
    float ins = smoothstep(0.11,.46,lp);
    float outs = .15+smoothstep(.0,.15,abs(lp-1.));
    p *= ins*outs;
    float id = ins*outs;
    
    float rz = segm(p, bg, en)-0.011;
    return vec2(rz,id);
}

float march(in vec3 ro, in vec3 rd, in float startf, in float maxd, in float j)
{
    float precis = 0.001;
    float h=0.5;
    float d = startf;
    for( int i=0; i<MAX_ITER; i++ )
    {
        if( abs(h)<precis||d>maxd ) break;
        d += h*1.2;
        float res = map(ro+rd*d, j).x;
        h = res;
    }
    return d;
}

//volumetric marching
vec3 vmarch(in vec3 ro, in vec3 rd, in float j, in vec3 orig)
{   
    vec3 p = ro;
    vec2 r = vec2(0.);
    vec3 sum = vec3(0);
    float w = 0.;
    for( int i=0; i<VOLUMETRIC_STEPS; i++ )
    {
        r = map(p,j);
        p += rd*.03;
        float lp = length(p);
        
        vec3 col = sin(vec3(1.05,2.5,1.52)*3.94+r.y)*.85+0.4;
        col.rgb *= smoothstep(.0,.015,-r.x);
        col *= smoothstep(0.04,.2,abs(lp-1.1));
        col *= smoothstep(0.1,.34,lp);
        sum += abs(col)*5. * (1.2-noise(lp*2.+j*13.+time*5.)*1.1) / (log(distance(p,orig)-2.)+.75);
    }
    return sum;
}

//returns both collision dists of unit sphere
vec2 iSphere2(in vec3 ro, in vec3 rd)
{
    vec3 oc = ro;
    float b = dot(oc, rd);
    float c = dot(oc,oc) - 1.;
    float h = b*b - c;
    if(h <0.0) return vec2(-1.);
    else return vec2((-b - sqrt(h)), (-b + sqrt(h)));
}

void mainImage( out vec4 fragColor, in vec2 fragCoord )
{	
    vec2 p = fragCoord.xy/iResolution.xy-0.5;
    p.x*=iResolution.x/iResolution.y;
    vec2 um = iMouse.xy / iResolution.xy-.5;
    
    //camera
    vec3 ro = vec3(0.,0.,5.);
    vec3 rd = normalize(vec3(p*.7,-1.5));
    mat2 mx = mm2(time*.4+um.x*6.);
    mat2 my = mm2(time*0.3+um.y*6.); 
    ro.xz *= mx;rd.xz *= mx;
    ro.xy *= my;rd.xy *= my;
    
    vec3 bro = ro;
    vec3 brd = rd;
	
    vec3 col = vec3(0.0125,0.,0.025);
    #if 1
    for (float j = 1.;j<NUM_RAYS+1.;j++)
    {
        ro = bro;
        rd = brd;
        mat2 mm = mm2((time*0.1+((j+1.)*5.1))*j*0.25);
        ro.xy *= mm;rd.xy *= mm;
        ro.xz *= mm;rd.xz *= mm;
        float rz = march(ro,rd,2.5,FAR,j);
		if (rz >= FAR)continue;
    	vec3 pos = ro+rz*rd;
    	col = max(col,vmarch(pos,rd,j, bro));
    }
    #endif
    
    vec2 sph = iSphere2(ro,rd);
    
    if(sph.x > 0.)
    {
        vec3 pos = ro+rd*sph.x;
        vec3 nor = pos;
        vec3 ligt = normalize(vec3(.5,.5,.5));
        vec3 col2 = textureLod(iChannel0,nor.xy,0.).rgb;
        float dif = clamp(dot(nor,ligt),0.,1.);
        vec3 brdf = dif*vec3(0.25,0.0,0.05);
        col2 = (col2+brdf);
        col = max(col,col2);
    }
    
    col = pow(col,vec3(0.55));
	fragColor = vec4(col,1.0);
}
"""

if __name__ == '__main__':
    # Criando renderizador com suporte a ShaderToy
    renderizador = Renderizador(resolution=(1024, 768), lock_mouse=False)
    renderizador.set_title("Demonstração de Compatibilidade com ShaderToy")
    
    # Defina o shader e o caminho para uma textura de ruído
    # (o ShaderToy acima usa iChannel0 como uma textura de ruído)
    base = os.path.dirname(os.path.abspath(__file__))
    texture_file = os.path.join(base, "texture/noise.jpg")
    
    # Verifique se o arquivo de textura existe
    if os.path.exists(texture_file):
        print(f"Usando textura de ruído: {texture_file}")
        renderizador.set_texture(texture_file, 0)
    else:
        # Se a textura não existir, tente criá-la
        print(f"Textura de ruído não encontrada em {texture_file}")
        print("Tentando criar uma textura de ruído temporária...")
        
        try:
            # Cria um diretório texture se não existir
            os.makedirs(os.path.join(base, "texture"), exist_ok=True)
            
            # Tenta importar PIL para criar a textura
            from PIL import Image
            import numpy as np
            
            # Gera uma textura de ruído simples
            width, height = 512, 512
            noise = np.random.rand(height, width) * 255
            noise = noise.astype(np.uint8)
            
            # Cria a imagem e salva
            noise_image = Image.fromarray(noise, mode='L')
            noise_image.save(texture_file, quality=90)
            print(f"Textura de ruído criada com sucesso em: {texture_file}")
            
            # Carrega a textura recém-criada
            renderizador.set_texture(texture_file, 0)
            
        except Exception as e:
            print(f"Não foi possível criar a textura de ruído: {e}")
            print("O shader pode não funcionar corretamente sem uma textura de ruído.")
            print("Para criar uma textura manualmente, execute: python exemplos/create_noise_texture.py")

    # Configura o shader do ShaderToy e renderiza
    renderizador.set_shaders(fragment_shader_source=SHADERTOY_CODE)
    renderizador.render()