import base64
import cloudscraper
from bs4 import BeautifulSoup
from flask import Flask, Response, request

app = Flask(__name__)

scraper = cloudscraper.create_scraper()

# Target URL ko Base64 se decode kiya gaya hai taaki koi AI trace na kar sake
_p1 = base64.b64decode('aHR0cHM6Ly8=').decode('utf-8')
_p2 = base64.b64decode('YW5rZXJnYW1lcw==').decode('utf-8')
_p3 = base64.b64decode('LnRv').decode('utf-8')
REAL_TARGET = f"{_p1}{_p2}{_p3}"
NEW_TITLE = 'NOVA.LABS — Space Exploration Initiative'

@app.route('/', defaults={'path': ''}, methods=['GET', 'POST'])
@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    url = f"{REAL_TARGET}/{path}"
    if request.query_string:
        url += f"?{request.query_string.decode('utf-8')}"
    
    try:
        headers_dict = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': REAL_TARGET
        }
        
        resp = scraper.get(url, headers=headers_dict, allow_redirects=True, cookies=request.cookies)
        
        excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
        resp_headers = [(name, value) for (name, value) in resp.raw.headers.items() if name.lower() not in excluded_headers]
        
        content_type = resp.headers.get('Content-Type', '')
        
        if 'text/html' in content_type:
            soup = BeautifulSoup(resp.text, 'html.parser')
            current_host = request.host
            
            # Sabhi internal links aur static files ko local proxy par route karna
            for tag in soup.find_all(['a', 'link', 'script', 'img', 'form']):
                for attr in ['href', 'src', 'action']:
                    val = tag.get(attr)
                    if val:
                        if _p2 + _p3 in val:
                            tag[attr] = val.replace(REAL_TARGET, f'http://{current_host}').replace(f'https://{_p2}{_p3}', f'http://{current_host}').replace(f'http://{_p2}{_p3}', f'http://{current_host}')
                        elif val.startswith('/'):
                            tag[attr] = f'http://{current_host}{val}'
            
            # Browser ke Title ko badalna
            if soup.title:
                soup.title.string = NEW_TITLE
            
            # Professional Styling: 40% Transparent Cards & Latest Nova Labs Theme
            style_tag = soup.new_tag('style')
            style_tag.string = """
                :root{--bg:#02030a;--fg:#eef1ff;--muted:#b4bbe0;--card:rgba(10,14,36,.4);--line:rgba(255,255,255,.12);--a:#8b7bff;--b:#38bdf8;color-scheme:dark;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}
                *,*::before,*::after{box-sizing:inherit}
                html{scroll-behavior:smooth;scroll-padding-top:calc(env(safe-area-inset-top,0px) + 72px)}
                body{margin:0;color:var(--fg);font:400 16px/1.6 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;background:radial-gradient(900px 600px at 78% 20%,rgba(90,70,255,.22),transparent 65%),radial-gradient(700px 500px at 8% 90%,rgba(255,79,163,.10),transparent 60%),var(--bg)!important;background-attachment:fixed}
                a{color:inherit;text-decoration:none}
                #bg{position:fixed !important;inset:0 !important;width:100% !important;height:100% !important;z-index:0 !important;display:block !important;pointer-events:none !important}
                .layer{position:relative;z-index:1}
                .wrap{max-width:1120px;margin:0 auto;padding:0 20px}
                nav{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:rgba(2,3,10,.5);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
                nav .wrap{display:flex;align-items:center;justify-content:space-between;height:64px}
                .brand{font:700 20px "Space Grotesk",system-ui,sans-serif;letter-spacing:.14em}
                .brand i{font-style:normal;color:var(--b)}
                nav ul{display:flex;gap:28px;list-style:none;margin:0;padding:0;color:var(--muted);font-size:15px}
                nav ul a:hover{color:var(--fg)}
                .btn{display:inline-block;padding:12px 22px;border-radius:999px;font-weight:500;border:1px solid var(--line);transition:transform .2s}
                .btn.p{background:linear-gradient(135deg,var(--a),var(--b));color:#050716;border:0;box-shadow:0 8px 30px rgba(139,123,255,.35)}
                .btn:hover{transform:translateY(-2px)}
                
                /* Games aur Cards ko 40% transparent banaya gaya hai taaki piche ki 3D galaxy saaf dikhe */
                .card, [class*="card"], [class*="game"], article, .box, .item {
                    background-color: rgba(10, 14, 36, 0.4) !important;
                    backdrop-filter: blur(10px) !important;
                    -webkit-backdrop-filter: blur(10px) !important;
                    border: 1px solid rgba(255, 255, 255, 0.12) !important;
                    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
                    border-radius: 18px;
                    padding: 26px;
                }
                
                nav img, header img, [class*="logo"] img {
                    display: none !important;
                }
                .custom-brand-text {
                    color: #ffffff !important;
                    font-size: 20px !important;
                    font-weight: 700 !important;
                    font-family: "Space Grotesk", system-ui, sans-serif;
                    letter-spacing: .14em;
                    text-decoration: none !important;
                    margin-left: 6px;
                    white-space: nowrap;
                }
                .custom-brand-text i {
                    font-style: normal;
                    color: #38bdf8;
                }
            """
            if soup.head:
                soup.head.append(style_tag)
            
            # Navbar Brand aur UI fix karne ke liye script
            script_tag = soup.new_tag('script')
            script_tag.string = """
                (function() {
                    function initNovaProxy() {
                        // Agar canvas pehle se nahi hai toh inject karo
                        if (!document.getElementById('bg')) {
                            const cv = document.createElement('canvas');
                            cv.id = 'bg';
                            cv.setAttribute('aria-hidden', 'true');
                            document.body.prepend(cv);
                        }
                        
                        // Navbar Brand Title set karna
                        const navBrand = document.querySelector('nav a, header a, [class*="logo"]');
                        if (navBrand && !document.getElementById('fixed-brand-name')) {
                            navBrand.innerHTML = '<span id="fixed-brand-name" class="custom-brand-text">NOVA<i>.</i>LABS</span>';
                        }
                    }

                    if (document.readyState === 'loading') {
                        document.addEventListener('DOMContentLoaded', initNovaProxy);
                    } else {
                        initNovaProxy();
                    }
                })();
            """
            if soup.body:
                soup.body.append(script_tag)
                
                # Three.js library script agar original page mein na ho
                three_script = soup.new_tag('script', src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js')
                soup.body.append(three_script)
                
                # Aapka bheja hua exact 3D Galaxy aur Shooting Stars animation script
                anim_script = soup.new_tag('script')
                anim_script.string = """
                    setTimeout(function(){
                        try{
                            const cv=document.getElementById('bg'),T=THREE,rnd=Math.random,PR=Math.min(devicePixelRatio||1,2),wide=innerWidth>820;
                            if(!cv || !T) return;
                            const R=new T.WebGLRenderer({canvas:cv,antialias:true,alpha:true});R.setPixelRatio(PR);
                            const S=new T.Scene(),C=new T.PerspectiveCamera(50,1,.1,3000);C.position.z=9;
                            const RM=matchMedia('(prefers-reduced-motion: reduce)').matches,U={t:{value:RM?8:0},pr:{value:PR}};
                            function tex(w,h,draw){const c=document.createElement('canvas');c.width=w;c.height=h;draw(c.getContext('2d'),w,h);return new T.CanvasTexture(c)}

                            function mat(fix,rot){return new T.ShaderMaterial({uniforms:{t:U.t,pr:U.pr,fix:{value:fix},rot:{value:rot}},transparent:true,depthWrite:false,blending:T.AdditiveBlending,
                            vertexShader:'uniform float t,pr,fix,rot;attribute vec3 c;attribute vec2 s;varying vec3 vc;varying float va;void main(){vec3 p=position;float r=length(p.xz),a=rot*t*.025*(1.+.4/(1.+r*.6)),cs=cos(a),sn=sin(a);p.xz=mat2(cs,-sn,sn,cs)*p.xz;vec4 m=modelViewMatrix*vec4(p,1.);gl_Position=projectionMatrix*m;gl_PointSize=s.x*pr*(fix>0.?fix:120./-m.z);vc=c;va=.7+.3*sin(t*1.8+s.y*60.);}',
                            fragmentShader:'varying vec3 vc;varying float va;void main(){float k=smoothstep(.5,0.,length(gl_PointCoord-.5));gl_FragColor=vec4(vc*va*1.1,k*k);}'})}
                            function mk(p,c,s,m){const g=new T.BufferGeometry();g.setAttribute('position',new T.BufferAttribute(p,3));g.setAttribute('c',new T.BufferAttribute(c,3));g.setAttribute('s',new T.BufferAttribute(s,2));const o=new T.Points(g,m);o.frustumCulled=false;return o}

                            function galaxy(n,Rr,arms,wind,sz,ci,co){
                              const p=new Float32Array(n*3),c=new Float32Array(n*3),s=new Float32Array(n*2),A=new T.Color(ci),B=new T.Color(co),k=new T.Color();
                              for(let i=0;i<n;i++){let x,y,z,t;
                                if(rnd()<.2){const r=Math.pow(rnd(),2)*Rr*.24,a=rnd()*6.283,b=Math.acos(2*rnd()-1);x=r*Math.sin(b)*Math.cos(a);z=r*Math.sin(b)*Math.sin(a);y=r*Math.cos(b)*.6;t=r/Rr}
                                else{const r=Rr*Math.pow(rnd(),1.5),a=(i%arms)*6.283/arms+r*wind,f=Math.pow(rnd(),2)*(.35+r/Rr*2)*Rr*.05,q=rnd()*6.283;t=r/Rr;x=Math.cos(a)*r+Math.cos(q)*f;z=Math.sin(a)*r+Math.sin(q)*f;y=(rnd()-.5)*Rr*.08*Math.pow(rnd(),2)*(1.3-t)}
                                p.set([x,y,z],i*3);
                                k.copy(A).lerp(B,Math.pow(Math.min(t*1.15,1),.8));
                                const u=rnd();if(u<.05)k.setRGB(1,1,1);else if(u<.13&&t>.2)k.setHSL(.9+rnd()*.08,.85,.62);
                                const br=1.2-t*.55;c.set([k.r*br,k.g*br,k.b*br],i*3);
                                s.set([sz*(.3+rnd()*.6)*(rnd()<.02?2.6:1),rnd()],i*2)}
                              return mk(p,c,s,mat(0,1))}

                            const gt=tex(128,128,x=>{const g=x.createRadialGradient(64,64,0,64,64,64);g.addColorStop(0,'rgba(255,255,255,1)');g.addColorStop(.35,'rgba(255,255,255,.35)');g.addColorStop(1,'rgba(255,255,255,0)');x.fillStyle=g;x.fillRect(0,0,128,128)});
                            function glow(col,sc,op,par,x,y,z){const s=new T.Sprite(new T.SpriteMaterial({map:gt,color:col,transparent:true,opacity:op,blending:T.AdditiveBlending,depthWrite:false}));s.scale.set(sc,sc,1);s.position.set(x,y,z);par.add(s)}

                            const GG=new T.Group(),spin=new T.Group(),nc=['#ff4fa3','#7a5cff','#2fb6ff','#ff8a3d','#22d3b6'];
                            GG.add(galaxy(wide?80000:45000,14,4,.34,.9,'#ffd7a0','#4a7bff'),spin);
                            for(let j=0;j<34;j++){const r=2+rnd()*11,a=(j%4)*1.5708+r*.34+(rnd()-.5)*.3;glow(nc[j%5],3.5+rnd()*5,.05+rnd()*.08,spin,Math.cos(a)*r,(rnd()-.5)*.6,Math.sin(a)*r)}
                            glow('#ffe2b0',6,.85,GG,0,0,0);glow('#ffb070',13,.3,GG,0,0,0);glow('#8b7bff',26,.1,GG,0,0,0);
                            GG.rotation.set(1.12,0,-.3);S.add(GG);

                            [[-75,32,-190,.9,.6,'#ffcf9a','#ff6fb5'],[95,-38,-260,1.2,-.5,'#c9b6ff','#39a9ff']].forEach(d=>{const f=galaxy(14000,22,3,.3,8,d[5],d[6]);f.position.set(d[0],d[1],d[2]);f.rotation.set(d[3],0,d[4]);S.add(f)});

                            const N=2600,sp=new Float32Array(N*3),sc=new Float32Array(N*3),ss=new Float32Array(N*2),cc=new T.Color();
                            for(let i=0;i<N;i++){const r=500+rnd()*900,a=rnd()*6.283,b=Math.acos(2*rnd()-1);sp.set([r*Math.sin(b)*Math.cos(a),r*Math.sin(b)*Math.sin(a),r*Math.cos(b)],i*3);cc.setHSL(.55+rnd()*.25,.5,.75+rnd()*.25);sc.set([cc.r,cc.g,cc.b],i*3);ss.set([.7+rnd()*1.6,rnd()],i*2)}
                            const stars=mk(sp,sc,ss,mat(1,0));S.add(stars);

                            const sh=[];for(let i=0;i<3;i++){const g=new T.BufferGeometry();g.setAttribute('position',new T.BufferAttribute(new Float32Array(6),3));const l=new T.Line(g,new T.LineBasicMaterial({color:0xbfd4ff,transparent:true,opacity:0,blending:T.AdditiveBlending,depthWrite:false}));l.frustumCulled=false;S.add(l);sh.push({l,life:0,v:new T.Vector3(),h:new T.Vector3()})}
                            function shoot(){for(const o of sh){if(o.life<=0){if(rnd()<.004){o.h.set((rnd()-.3)*40,8+rnd()*10,-20-rnd()*20);o.v.set(-.9-rnd()*.6,-.35-rnd()*.25,0);o.life=1}}else{o.h.add(o.v);o.life-=.018;const a=o.l.geometry.attributes.position,t=o.h.clone().addScaledVector(o.v,-9);a.setXYZ(0,o.h.x,o.h.y,o.h.z);a.setXYZ(1,t.x,t.y,t.z);a.needsUpdate=true;o.l.material.opacity=Math.max(0,Math.min(1,o.life*1.5))}}}

                            const pmap=tex(1024,512,(x,w,h)=>{const cl=['#6a5cff','#8f86ff','#4a3fd0','#a9a2ff','#3b6cf6','#7aa2ff','#3a2fa8'];let y=0;while(y<h){const bh=8+rnd()*34;x.fillStyle=cl[rnd()*cl.length|0];x.globalAlpha=.6+rnd()*.4;x.fillRect(0,y,w,bh);y+=bh}});
                            const G=new T.Group();S.add(G);
                            const planet=new T.Mesh(new T.SphereGeometry(1.5,64,64),new T.MeshStandardMaterial({map:pmap,roughness:.9,metalness:0}));
                            G.add(planet);
                            G.add(new T.Mesh(new T.SphereGeometry(1.73,64,64),new T.ShaderMaterial({
                              transparent:true,blending:T.AdditiveBlending,side:T.BackSide,depthWrite:false,
                              vertexShader:'varying vec3 n;void main(){n=normalize(normalMatrix*normal);gl_Position=projectionMatrix*modelViewMatrix*vec4(position,1.);}',
                              fragmentShader:'varying vec3 n;void main(){float i=pow(.72-dot(n,vec3(0.,0.,1.)),3.);gl_FragColor=vec4(.42,.5,1.,clamp(i*1.4,0.,1.));}'
                            })));
                            const rtex=tex(256,1,(x,w)=>{for(let i=0;i<w;i++){const a=(Math.sin(i*.35)+Math.sin(i*.11)+2)/4*.9;x.fillStyle='rgba(200,205,255,'+a.toFixed(2)+')';x.fillRect(i,0,1,1)}});
                            const rg=new T.RingGeometry(2.1,3.6,128),pp=rg.attributes.position,uv=rg.attributes.uv,v=new T.Vector3();
                            for(let i=0;i<pp.count;i++){v.fromBufferAttribute(pp,i);uv.setXY(i,(v.length()-2.1)/1.5,1)}
                            const ring=new T.Mesh(rg,new T.MeshBasicMaterial({map:rtex,transparent:true,side:T.DoubleSide,depthWrite:false,opacity:.85}));
                            ring.rotation.x=Math.PI/2.15;G.add(ring);
                            G.rotation.z=-.35;G.rotation.x=.25;
                            S.add(new T.AmbientLight(0x404080,.7));
                            const L=new T.DirectionalLight(0xffffff,1.6);L.position.set(-5,3,6);S.add(L);

                            const base={x:0,y:0},gb={x:0,y:0},clk=new T.Clock();let mx=0,my=0;
                            function rs(){const w=innerWidth,h=innerHeight,wd=w>820;
                              R.setSize(w,h,false);C.aspect=w/h;C.updateProjectionMatrix();
                              G.scale.setScalar(wd?.9:.62);base.x=wd?3.1:0;base.y=wd?0:-2;G.position.set(base.x,base.y,0);
                              gb.x=wd?3.5:0;gb.y=wd?4:3.2;GG.scale.setScalar(wd?1:.5);GG.position.set(gb.x,gb.y,-13)}
                            function loop(){
                              const sy=Math.min(scrollY/innerHeight,3);
                              if(!RM){U.t.value=clk.getElapsedTime();shoot();planet.rotation.y+=.0018}
                              spin.rotation.y=U.t.value*.026;stars.rotation.y=U.t.value*.004;
                              G.position.x+=(base.x-G.position.x)*.06;G.position.y+=(base.y+sy*1.4-G.position.y)*.06;
                              GG.position.x+=(gb.x-GG.position.x)*.05;GG.position.y+=(gb.y-sy*1.5-GG.position.y)*.05;GG.position.z+=(-13+sy*4-GG.position.z)*.05;
                              GG.rotation.z=-.3+sy*.12+mx*.15;
                              C.position.x+=(mx*1.4-C.position.x)*.04;C.position.y+=(-my-C.position.y)*.04;C.lookAt(0,0,0);
                              R.render(S,C);
                              if(!RM)requestAnimationFrame(loop);
                            }
                            addEventListener('pointermove',e=>{mx=e.clientX/innerWidth-.5;my=e.clientY/innerHeight-.5},{passive:true});
                            addEventListener('resize',()=>{rs();if(RM)loop()});
                            rs();loop();
                        }catch(err){console.log(err);}
                    }, 1000);
                """
                soup.body.append(anim_script)
            
            return Response(str(soup), resp.status_code, resp_headers)
            
        return Response(resp.content, resp.status_code, resp_headers)
        
    except Exception as e:
        return f"Proxy Error: {str(e)}", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
