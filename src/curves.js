// Local cubic fitting. This is original code; no model or font outlines are used.
function segmentDistance(p,a,b){const dx=b[0]-a[0],dy=b[1]-a[1],u=Math.max(0,Math.min(1,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/(dx*dx+dy*dy||1)));return Math.hypot(p[0]-a[0]-u*dx,p[1]-a[1]-u*dy);}
function ringDeviation(a,b){let worst=0;for(const p of a){let best=Infinity;for(let i=1;i<b.length;i++)best=Math.min(best,segmentDistance(p,b[i-1],b[i]));worst=Math.max(worst,best);}return worst;}
function shapeDeviation(a,b){return Math.max(ringDeviation(a,b),ringDeviation(b,a));}
function cubicValue(a,b,c,d,t){const u=1-t;return [0,1].map(k=>u*u*u*a[k]+3*u*u*t*b[k]+3*u*t*t*c[k]+t*t*t*d[k]);}
function unitVector(a){const n=Math.hypot(...a)||1;return a.map(v=>v/n);}
function fitCubicRun(points,tolerance,startTangent,endTangent,depth=0){
 const first=points[0],last=points.at(-1);
 if(points.length<3)return [L(...last)];
 if(points.every(p=>segmentDistance(p,first,last)<=tolerance))return [L(...last)];
 const u=[0];for(let i=1;i<points.length;i++)u.push(u.at(-1)+Math.hypot(points[i][0]-points[i-1][0],points[i][1]-points[i-1][1]));
 const total=u.at(-1)||1;for(let i=0;i<u.length;i++)u[i]/=total;
 const left=startTangent||unitVector([points[1][0]-first[0],points[1][1]-first[1]]),right=endTangent||unitVector([points.at(-2)[0]-last[0],points.at(-2)[1]-last[1]]);
 let aa=0,ab=0,bb=0,ax=0,bx=0;
 points.forEach((p,i)=>{const t=u[i],v=1-t,b0=v*v*v,b1=3*t*v*v,b2=3*t*t*v,b3=t*t*t,A=left.map(x=>x*b1),B=right.map(x=>x*b2),R=p.map((x,k)=>x-first[k]*(b0+b1)-last[k]*(b2+b3));aa+=A[0]**2+A[1]**2;ab+=A[0]*B[0]+A[1]*B[1];bb+=B[0]**2+B[1]**2;ax+=A[0]*R[0]+A[1]*R[1];bx+=B[0]*R[0]+B[1]*R[1];});
 const determinant=aa*bb-ab*ab,distance=Math.hypot(last[0]-first[0],last[1]-first[1]);let alpha=(ax*bb-bx*ab)/(determinant||1),beta=(bx*aa-ax*ab)/(determinant||1);
 if(alpha<=distance*.001||beta<=distance*.001||alpha>total*2||beta>total*2||Math.abs(determinant)<1e-12)alpha=beta=distance/3;
 const cp1=first.map((x,k)=>x+left[k]*alpha),cp2=last.map((x,k)=>x+right[k]*beta);let worst=0,split=Math.floor(points.length/2);
 points.forEach((p,i)=>{const q=cubicValue(first,cp1,cp2,last,u[i]),error=Math.hypot(p[0]-q[0],p[1]-q[1]);if(error>worst){worst=error;split=i;}});
 if(worst<=tolerance)return [C(...cp1,...cp2,...last)];
 if(depth>12||split<1||split>=points.length-1)return points.slice(1).map(p=>L(...p));
 const tangent=unitVector([points[split+1][0]-points[split-1][0],points[split+1][1]-points[split-1][1]]);
 return [...fitCubicRun(points.slice(0,split+1),tolerance,left,tangent.map(v=>-v),depth+1),...fitCubicRun(points.slice(split),tolerance,tangent,right,depth+1)];
}
function compactRing(r,tolerance=1){
 const points=r.slice(0,-1);if(points.length<5)return [M(...points[0]),...points.slice(1).map(p=>L(...p)),Z()];
 const xs=points.map(p=>p[0]),ys=points.map(p=>p[1]),x=Math.min(...xs),y=Math.min(...ys),w=Math.max(...xs)-x,h=Math.max(...ys)-y;
 if(w>2&&h>2){const ellipse=oval(x,y,w,h),flat=flatten([ellipse],.15)[0];if(shapeDeviation(r,flat)<=tolerance&&!contourIssues({contours:quantize([ellipse])}).length)return area(r)>0?ellipse:reverseContour(ellipse);}
 const corners=[];for(let i=0;i<points.length;i++){const a=points[(i+points.length-1)%points.length],b=points[i],c=points[(i+1)%points.length],u=unitVector([b[0]-a[0],b[1]-a[1]]),v=unitVector([c[0]-b[0],c[1]-b[1]]);if(Math.acos(Math.max(-1,Math.min(1,u[0]*v[0]+u[1]*v[1])))>.6)corners.push(i);}
 const cuts=corners.length?corners:[0,Math.floor(points.length/4),Math.floor(points.length/2),Math.floor(points.length*3/4)];const out=[M(...points[cuts[0]])];
 for(let k=0;k<cuts.length;k++){const from=cuts[k],to=cuts[(k+1)%cuts.length],run=[points[from]];let i=(from+1)%points.length;while(i!==to){run.push(points[i]);i=(i+1)%points.length;}run.push(points[to]);let start,end;if(!corners.length){const prev=points[(from+points.length-1)%points.length],next=points[(from+1)%points.length];start=unitVector([next[0]-prev[0],next[1]-prev[1]]);const before=points[(to+points.length-1)%points.length],after=points[(to+1)%points.length];end=unitVector([before[0]-after[0],before[1]-after[1]]);}out.push(...fitCubicRun(run,tolerance*.7,start,end));}
 out.push(Z());const flat=flatten([out],.15)[0];if(!flat||contourIssues({contours:quantize([out])}).length||shapeDeviation(r,flat)>tolerance*1.25||Math.sign(area(flat))!==Math.sign(area(r)))return [M(...points[0]),...points.slice(1).map(p=>L(...p)),Z()];return out;
}
function curvedBoolean(polygons,originals,tolerance=.8){
 const sources=originals.map(path=>({path,ring:flatten([path],.6)[0]})).filter(s=>s.ring);
 return polygons.flatMap(poly=>poly.map((ring,index)=>{let r=ring;if((area(r)>0)!==(index===0))r=[...r].reverse();
  // Unchanged counters and complete curves retain their actual Bézier controls.
  const intact=sources.find(s=>Math.abs(Math.abs(area(s.ring))-Math.abs(area(r)))<.01&&shapeDeviation(r,s.ring)<.001);
  if(intact)return (area(intact.ring)>0)===(index===0)?clone(intact.path):reverseContour(intact.path);
  return compactRing(r,tolerance);
 }));
}
function countNodes(contours){return contours.reduce((n,p)=>{const pts=p.filter(c=>c.type!=='Z'),closed=p.at(-1)?.type==='Z',duplicate=closed&&pts.length>1&&pts[0].x===pts.at(-1).x&&pts[0].y===pts.at(-1).y;return n+pts.length-(duplicate?1:0);},0);}
function reduceContours(contours,tolerance=1){return contours.map(p=>{if(p.at(-1)?.type!=='Z')throw Error('Feche o contorno antes de reduzir os nós.');if(countNodes([p])<=8&&p.some(c=>c.type==='C'))return clone(p);const ring=flatten([p],Math.min(.25,tolerance/3))[0];return compactRing(ring,tolerance);});}
function repairRoundedJunctions(contours){
 const result=clone(contours);let removed=0;
 for(const path of result){for(let i=1;i<path.length-1;i++){const prev=path[i-1],c=path[i];if(c.type==='L'&&prev.x!==undefined&&Math.hypot(c.x-prev.x,c.y-prev.y)<=1.5){path.splice(i,1);removed++;i--;}}}
 if(!removed||contourIssues({contours:result}).length)return null;
 const error=Math.max(...contours.map((p,i)=>shapeDeviation(flatten([p],.2)[0],flatten([result[i]],.2)[0])));
 return error<=1.5?{contours:result,removed,error}:null;
}
