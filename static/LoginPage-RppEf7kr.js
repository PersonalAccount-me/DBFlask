import{_ as x,i as k,B as y,C as _,o as C,g as E,b as a,w as r,u as o,a as i,a2 as B,a3 as p,v as I,a4 as M,s as R,p as F,f as L,d as l}from"./index-nrIvu4tl.js";import{E as P,a as S}from"./el-form-item-yRykdAuK.js";/* empty css                   */const f=n=>(F("data-v-441a7365"),n=n(),L(),n),U={class:"login"},j=f(()=>l("svg",{class:"icon",xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 1024 1024","data-v-ea893728":""},[l("path",{fill:"currentColor",d:"M512 512a192 192 0 1 0 0-384 192 192 0 0 0 0 384m0 64a256 256 0 1 1 0-512 256 256 0 0 1 0 512m320 320v-96a96 96 0 0 0-96-96H288a96 96 0 0 0-96 96v96a32 32 0 1 1-64 0v-96a160 160 0 0 1 160-160h448a160 160 0 0 1 160 160v96a32 32 0 1 1-64 0"})],-1)),H=f(()=>l("svg",{xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 1024 1024","data-v-ea893728":"",class:"icon"},[l("path",{fill:"currentColor",d:"M224 448a32 32 0 0 0-32 32v384a32 32 0 0 0 32 32h576a32 32 0 0 0 32-32V480a32 32 0 0 0-32-32zm0-64h576a96 96 0 0 1 96 96v384a96 96 0 0 1-96 96H224a96 96 0 0 1-96-96V480a96 96 0 0 1 96-96"}),l("path",{fill:"currentColor",d:"M512 544a32 32 0 0 1 32 32v192a32 32 0 1 1-64 0V576a32 32 0 0 1 32-32m192-160v-64a192 192 0 1 0-384 0v64zM512 64a256 256 0 0 1 256 256v128H256V320A256 256 0 0 1 512 64"})],-1)),N={__name:"LoginPage",setup(n){const g=k("skipPage"),u=y(null);let s=_({username:"",password:"",isRemember:!1});const v=_({username:[{required:!0,message:"账号输入不能为空！",trigger:"blur"}],password:[{required:!0,message:"密码输入不能为空！",trigger:"blur"}]}),h=()=>{u.value.validate().then(m=>{B.post("/log/login",s,{headers:{"Content-Type":"application/json;charset=UTF-8"}}).then(({data:e})=>{switch(e.isLogin){case!0:{p({type:"success",message:"登陆成功！！"}),g("main");break}case!1:{p({type:"error",message:"登陆失败！请检查您的账号或密码输入正确"});break}}}).catch(({message:e})=>{p({type:"error",message:"网络错误！"})})}).catch(m=>{const e=m[Object.keys(m)[0]][0].message;p({type:"error",message:e})})};return(m,e)=>{const d=I,c=S,w=M,b=R,V=P;return C(),E("div",U,[a(V,{"status-icon":"",ref_key:"formRef",ref:u,rules:v,model:o(s)},{default:r(()=>[a(c,{prop:"username",class:"form-item"},{default:r(()=>[j,i("： "),a(d,{class:"info-input",type:"text",modelValue:o(s).username,"onUpdate:modelValue":e[0]||(e[0]=t=>o(s).username=t),placeholder:"请输入账号"},null,8,["modelValue"])]),_:1}),a(c,{prop:"password",class:"form-item"},{default:r(()=>[H,i("： "),a(d,{class:"info-input",type:"password",modelValue:o(s).password,"onUpdate:modelValue":e[1]||(e[1]=t=>o(s).password=t),placeholder:"请输入密码"},null,8,["modelValue"])]),_:1}),a(c,{prop:"isRemember",class:"form-item"},{default:r(()=>[a(w,{label:"记住密码",name:"type",class:"psd-checkbox",modelValue:o(s).isRemember,"onUpdate:modelValue":e[2]||(e[2]=t=>o(s).isRemember=t)},null,8,["modelValue"])]),_:1}),a(b,{class:"submit-btn",type:"primary",onClick:e[3]||(e[3]=t=>h())},{default:r(()=>[i("登录")]),_:1})]),_:1},8,["rules","model"])])}}},A=x(N,[["__scopeId","data-v-441a7365"]]);export{A as default};