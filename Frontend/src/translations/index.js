import en from './en.json';
import hi from './hi.json';
import bn from './bn.json';
import te from './te.json';
import ta from './ta.json';
import mr from './mr.json';
import gu from './gu.json';
import kn from './kn.json';
import ml from './ml.json';
import or from './or.json';

export const translations = {
  en,
  hi,
  bn,
  te,
  ta,
  mr,
  gu,
  kn,
  ml,
  or
};

export const getTranslation = (key, language = 'en') => {
  const keys = key.split('.');
  let value = translations[language];
  
  for (const k of keys) {
    value = value?.[k];
    if (value === undefined) break;
  }
  
  // Fallback to English if translation not found
  if (value === undefined && language !== 'en') {
    let enValue = translations.en;
    for (const k of keys) {
      enValue = enValue?.[k];
      if (enValue === undefined) break;
    }
    value = enValue;
  }
  
  return value || key;
};