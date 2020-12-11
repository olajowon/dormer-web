/**
 * Created by zhouwang on 2020/12/10.
 */


export function formatDatetime(fmt, dt){
  let ret;
  const opt = {
      "Y+": dt.getFullYear().toString(),        // 年
      "m+": (dt.getMonth() + 1).toString(),     // 月
      "d+": dt.getDate().toString(),            // 日
      "H+": dt.getHours().toString(),           // 时
      "M+": dt.getMinutes().toString(),         // 分
      "S+": dt.getSeconds().toString()          // 秒
  };
  for (let k in opt) {
      ret = new RegExp("(" + k + ")").exec(fmt);
      if (ret) {
          fmt = fmt.replace(ret[1], (ret[1].length == 1) ? (opt[k]) : (opt[k].padStart(ret[1].length, "0")))
      };
  };
  return fmt;
}


export function parseDatetime(fmt, sdt){
}



