import React, { createContext, useContext, useState, useEffect } from 'react';
import { translations, getTranslation } from '../translations';

const LanguageContext = createContext();

export const useLanguage = () => {
  const context = useContext(LanguageContext);
  if (!context) {
    throw new Error('useLanguage must be used within LanguageProvider');
  }
  return context;
};

export const LanguageProvider = ({ children }) => {
  const [language, setLanguage] = useState(() => {
    return localStorage.getItem('preferred-language') || 'en';
  });

  useEffect(() => {
    localStorage.setItem('preferred-language', language);
    // Trigger custom event for language change
    window.dispatchEvent(new CustomEvent('languageChanged', { detail: language }));
  }, [language]);

  const languages = {
    en: { name: 'English', code: 'en', nativeName: 'English' },
    hi: { name: 'Hindi', code: 'hi', nativeName: 'हिन्दी' },
    bn: { name: 'Bengali', code: 'bn', nativeName: 'বাংলা' },
    te: { name: 'Telugu', code: 'te', nativeName: 'తెలుగు' },
    ta: { name: 'Tamil', code: 'ta', nativeName: 'தமிழ்' },
    mr: { name: 'Marathi', code: 'mr', nativeName: 'मराठी' },
    gu: { name: 'Gujarati', code: 'gu', nativeName: 'ગુજરાતી' },
    kn: { name: 'Kannada', code: 'kn', nativeName: 'ಕನ್ನಡ' },
    ml: { name: 'Malayalam', code: 'ml', nativeName: 'മലയാളം' },
    or: { name: 'Odia', code: 'or', nativeName: 'ଓଡ଼ିଆ' }
  };

  const t = (key) => getTranslation(key, language);

  return (
    <LanguageContext.Provider value={{ 
      language, 
      setLanguage, 
      languages, 
      t,
      currentLanguage: languages[language]
    }}>
      {children}
    </LanguageContext.Provider>
  );
};