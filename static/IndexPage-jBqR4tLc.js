import{_ as T,i as B,aV as N,C as f,G as j,o as c,g as _,d as o,b as s,w as r,u as l,a3 as p,a2 as w,b1 as O,v as U,s as G,a9 as x,aX as y,c as V,a as P,b7 as R,p as A,f as D,b0 as F}from"./index-nrIvu4tl.js";import{u as H}from"./dataobj-gzktrDxi.js";/* empty css                   */const v=u=>(A("data-v-0c79175b"),u=u(),D(),u),L={class:"index-page"},M=v(()=>o("div",{class:"title"},[o("h1",null,"创建索引")],-1)),X={class:"create-form"},$={class:"create-form-item"},q=v(()=>o("div",{class:"text"}," CREATE ",-1)),z={class:"create-form-item"},J=v(()=>o("div",{class:"text"},"ON",-1)),K={class:"create-form-item"},Q={__name:"IndexPage",setup(u){const h=B("update"),b=H(),{indexNames:I,tableNames:g}=N(b),{getTableColumns:E}=b;let n=f({name:"",columns:[]}),a=f({name:"",column:"",type:""});j(()=>n.name,m=>{n.columns=E(m)});const S=()=>{I.value.includes(a.name)?(p({type:"error",message:"索引已存在！！"}),a.name=""):a.name===""||n.name===""||a.column===""?p({type:"error",message:"信息不全，无法创建！"}):w.post("create/index",{index_name:a.name,index_type:a.type,table_name:n.name,column:a.column},{headers:{"Content-Type":"application/json"}}).then(({data:{isCreated:m,message:t}})=>{m?(p({type:"success",message:"索引创建成功！！"}),h(),indexName.value=indexType.value=tableName.value=basedColumn.value=""):p({type:"error",message:t})})};return(m,t)=>{const d=F,i=O,k=U,C=G;return c(),_("div",L,[M,o("div",X,[o("div",$,[q,s(i,{class:"select-type",modelValue:l(a).type,"onUpdate:modelValue":t[0]||(t[0]=e=>l(a).type=e),placeholder:"索引类型"},{default:r(()=>[s(d,{label:"二叉树索引",value:"BSTIndex"}),s(d,{label:"哈希索引",value:"HashIndex"}),s(d,{label:"分组索引",value:"GroupIndex"})]),_:1},8,["modelValue"]),s(k,{class:"input-name",modelValue:l(a).name,"onUpdate:modelValue":t[1]||(t[1]=e=>l(a).name=e),placeholder:"索引名称"},null,8,["modelValue"])]),o("div",z,[J,s(i,{class:"select-table",modelValue:l(n).name,"onUpdate:modelValue":t[2]||(t[2]=e=>l(n).name=e),placeholder:"选择表"},{default:r(()=>[(c(!0),_(x,null,y(l(g),e=>(c(),V(d,{value:e,label:e,key:e},null,8,["value","label"]))),128))]),_:1},8,["modelValue"]),s(i,{class:"select-column",modelValue:l(a).column,"onUpdate:modelValue":t[3]||(t[3]=e=>l(a).column=e),placeholder:"基本列"},{default:r(()=>[(c(!0),_(x,null,y(l(n).columns,e=>(c(),V(d,{value:e,label:e,key:e},null,8,["value","label"]))),128))]),_:1},8,["modelValue"])]),o("div",K,[s(C,{type:"primary",onClick:t[4]||(t[4]=e=>S()),class:"submit-btn",icon:l(R)},{default:r(()=>[P("创建索引")]),_:1},8,["icon"])])])])}}},ee=T(Q,[["__scopeId","data-v-0c79175b"]]);export{ee as default};
