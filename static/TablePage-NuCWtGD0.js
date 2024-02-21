import{_ as M,i as P,aV as w,B as D,C as U,ad as V,A as H,o,g as u,d as s,b as a,u as n,aY as Q,a9 as h,aX as k,w as c,a3 as b,a2 as q,v as X,s as z,a as f,b4 as x,b5 as R,c as S,b7 as J,p as W,f as Z,b0 as ee,b1 as ae,a4 as le,a$ as te}from"./index-nrIvu4tl.js";/* empty css                          */import{u as se}from"./dataobj-gzktrDxi.js";/* empty css                   */const E=v=>(W("data-v-fe8c2fb9"),v=v(),Z(),v),oe={class:"table-page un-copy"},ne=E(()=>s("div",{class:"title"},[s("h1",null,"创建基本表")],-1)),ce={class:"create-form"},de={class:"create-form-item"},ue=E(()=>s("div",{class:"text"},"CREATE TABLE",-1)),re={class:"constraints-container"},me={class:"change-column-item"},pe=E(()=>s("div",{class:"text"},"FOREIGN KEY",-1)),ie=E(()=>s("div",{class:"text"},"REFERENCES",-1)),_e={class:"change-foreign-item"},be={class:"submit-table-info"},fe={__name:"TablePage",setup(v){const O=P("update"),C=se();let{tableNames:I}=w(C);const{getTableColumns:A}=C;let d=D(""),r=U([{name:"",type:"",constraints:[],key:V(16)}]);const B=()=>{r.push({name:"",type:"",constraints:[],key:V(16)})},L=()=>{r.length===1?b({type:"error",message:"表需要有主键"}):r.pop()};let m=U([{name:"",table:"",column:"",key:V(16)}]);const Y=()=>{m.push({name:"",table:"",column:"",key:V(16)})},F=H(()=>m.map(i=>A(i.table))),G=()=>{m.length===0?b({type:"error",message:"无效操作"}):m.pop()},K=()=>r[0].name,$=()=>{I.value.includes(d.value)?(b({type:"error",message:"表已存在！！"}),d.value=""):d.value===""?b({type:"error",message:"表名不能为空"}):q.post("/create/table",{tableName:d.value,primaryKey:K(),columnUnits:r,foreignUnits:m},{headers:{"Content-Type":"application/json"}}).then(i=>{b({type:"success",message:"创建成功！！"}),O()}).catch(i=>{console.log(i)})};return(i,t)=>{const g=X,p=ee,N=ae,y=le,j=te,_=z;return o(),u("div",oe,[ne,s("div",ce,[s("section",de,[ue,a(g,{placeholder:"表名",class:"table-name",modelValue:n(d),"onUpdate:modelValue":t[0]||(t[0]=e=>Q(d)?d.value=e:d=e)},null,8,["modelValue"])]),(o(!0),u(h,null,k(n(r),(e,T)=>(o(),u("section",{class:"create-form-item",key:e.key},[a(g,{placeholder:"列名",class:"column-name",modelValue:e.name,"onUpdate:modelValue":l=>e.name=l},null,8,["modelValue","onUpdate:modelValue"]),a(N,{placeholder:"数据类型",class:"select-data-type",modelValue:e.type,"onUpdate:modelValue":l=>e.type=l},{default:c(()=>[a(p,{label:"整型",value:"INT"}),a(p,{label:"小数型",value:"DECIMAL"}),a(p,{label:"字符型",value:"STRING"}),a(p,{label:"日期型",value:"DATE"})]),_:2},1032,["modelValue","onUpdate:modelValue"]),s("div",re,[a(j,{modelValue:e.constraints,"onUpdate:modelValue":l=>e.constraints=l},{default:c(()=>[a(y,{label:"PRIMARY KEY",value:"PRIMARY kEY"}),a(y,{label:"NOT NULL",value:"NOT NULL"}),a(y,{label:"UNIQUE",value:"UNIQUE"}),a(y,{label:"NOTHING",value:"NOTHING"})]),_:2},1032,["modelValue","onUpdate:modelValue"])])]))),128)),s("section",me,[a(_,{type:"success",onClick:t[1]||(t[1]=e=>B()),class:"add-btn",icon:n(x)},{default:c(()=>[f("添加列")]),_:1},8,["icon"]),a(_,{type:"danger",onClick:t[2]||(t[2]=e=>L()),class:"delete-btn",icon:n(R)},{default:c(()=>[f("删除列")]),_:1},8,["icon"])]),(o(!0),u(h,null,k(n(m),(e,T)=>(o(),u("section",{class:"foreign-key-item",key:e.key},[pe,a(g,{placeholder:"外键属性",class:"foreign-key-name",modelValue:e.name,"onUpdate:modelValue":l=>e.name=l},null,8,["modelValue","onUpdate:modelValue"]),ie,a(N,{placeholder:"表名",class:"refer-table-name",modelValue:e.table,"onUpdate:modelValue":l=>e.table=l},{default:c(()=>[(o(!0),u(h,null,k(n(I),l=>(o(),S(p,{value:l,label:l},null,8,["value","label"]))),256))]),_:2},1032,["modelValue","onUpdate:modelValue"]),a(N,{placeholder:"列名",class:"refer-table-column",modelValue:e.column,"onUpdate:modelValue":l=>e.column=l},{default:c(()=>[(o(!0),u(h,null,k(F.value[T],l=>(o(),S(p,{label:l,value:l},null,8,["label","value"]))),256))]),_:2},1032,["modelValue","onUpdate:modelValue"])]))),128)),s("section",_e,[a(_,{type:"success",onClick:t[3]||(t[3]=e=>Y()),class:"add-btn",icon:n(x)},{default:c(()=>[f("添加外键")]),_:1},8,["icon"]),a(_,{type:"danger",onClick:t[4]||(t[4]=e=>G()),class:"delete-btn",icon:n(R)},{default:c(()=>[f("删除外键")]),_:1},8,["icon"])]),s("section",be,[a(_,{class:"submit-btn",type:"primary",onClick:t[5]||(t[5]=e=>$()),icon:n(J)},{default:c(()=>[f("创建表")]),_:1},8,["icon"])])])])}}},ke=M(fe,[["__scopeId","data-v-fe8c2fb9"]]);export{ke as default};