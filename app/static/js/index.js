

function getDefaultLocale() {
  let lang = navigator.languages;
  if (lang !== undefined) {
    return lang[0];
  }
  return lang;
}

function switchLocale(locale) {
  return locale === 'ar' ? 'en' : 'ar';
}
console.log(getDefaultLocale());
