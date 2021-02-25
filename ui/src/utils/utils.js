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


export function getCookie(name) {
   let value = '; ' + document.cookie;
   let parts = value.split('; ' + name + '=');
   if (parts.length === 2) {
       return parts.pop().split(';').shift();
   }
}

export function checkQueryFromUntil(query) {
  if (!query.from && !query.until) {
    let lsFrom = localStorage.getItem("from")
    let lsUntil = localStorage.getItem("until")
    if (lsFrom || lsUntil) {
      query.from = lsFrom
      query.until = lsUntil
    } else {
      query.from = "-1h"
      query.until = "now"
    }
  }
}

export function checkQueryRefresh(query) {
  if (!query.refresh) {
    let lsRefresh = localStorage.getItem("refresh")
    if (lsRefresh) {
      query.refresh = lsRefresh
    } else {
      query.refresh = "0"
    }
  }
}
