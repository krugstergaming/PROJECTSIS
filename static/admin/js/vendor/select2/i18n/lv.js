<<<<<<< Updated upstream
/*! Select2 4.0.7 | https://github.com/select2/select2/blob/master/LICENSE.md */

(function(){if(jQuery&&jQuery.fn&&jQuery.fn.select2&&jQuery.fn.select2.amd)var e=jQuery.fn.select2.amd;return e.define("select2/i18n/lv",[],function(){function e(e,t,n,r){return e===11?t:e%10===1?n:r}return{inputTooLong:function(t){var n=t.input.length-t.maximum,r="Lūdzu ievadiet par  "+n;return r+=" simbol"+e(n,"iem","u","iem"),r+" mazāk"},inputTooShort:function(t){var n=t.minimum-t.input.length,r="Lūdzu ievadiet vēl "+n;return r+=" simbol"+e(n,"us","u","us"),r},loadingMore:function(){return"Datu ielāde…"},maximumSelected:function(t){var n="Jūs varat izvēlēties ne vairāk kā "+t.maximum;return n+=" element"+e(t.maximum,"us","u","us"),n},noResults:function(){return"Sakritību nav"},searching:function(){return"Meklēšana…"},removeAllItems:function(){return"Noņemt visus vienumus"}}}),{define:e.define,require:e.require}})();
=======
/*! Select2 4.0.13 | https://github.com/select2/select2/blob/master/LICENSE.md */

!function(){if(jQuery&&jQuery.fn&&jQuery.fn.select2&&jQuery.fn.select2.amd)var e=jQuery.fn.select2.amd;e.define("select2/i18n/lv",[],function(){function e(e,n,u,i){return 11===e?n:e%10==1?u:i}return{inputTooLong:function(n){var u=n.input.length-n.maximum,i="Lūdzu ievadiet par  "+u;return(i+=" simbol"+e(u,"iem","u","iem"))+" mazāk"},inputTooShort:function(n){var u=n.minimum-n.input.length,i="Lūdzu ievadiet vēl "+u;return i+=" simbol"+e(u,"us","u","us")},loadingMore:function(){return"Datu ielāde…"},maximumSelected:function(n){var u="Jūs varat izvēlēties ne vairāk kā "+n.maximum;return u+=" element"+e(n.maximum,"us","u","us")},noResults:function(){return"Sakritību nav"},searching:function(){return"Meklēšana…"},removeAllItems:function(){return"Noņemt visus vienumus"}}}),e.define,e.require}();
>>>>>>> Stashed changes
