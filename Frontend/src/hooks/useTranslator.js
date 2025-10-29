import { useState } from 'react';
import { useLanguage } from '../context/LanguageContext';

export const useTranslator = () => {
  const { language } = useLanguage();
  const [isTranslating, setIsTranslating] = useState(false);

  const translateText = async (text, targetLang = language) => {
    if (!text || targetLang === 'en') return text;
    
    try {
      setIsTranslating(true);
      const response = await fetch('http://localhost:8000/api/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          text: text,
          target_lang: targetLang
        })
      });

      if (!response.ok) {
        throw new Error('Translation failed');
      }

      const data = await response.json();
      return data.translated_text || text;
    } catch (error) {
      console.error('Translation error:', error);
      return text; // Return original text if translation fails
    } finally {
      setIsTranslating(false);
    }
  };

  const translateObject = async (obj, targetLang = language) => {
    if (targetLang === 'en') return obj;
    
    const translated = {};
    for (const [key, value] of Object.entries(obj)) {
      if (typeof value === 'string') {
        translated[key] = await translateText(value, targetLang);
      } else if (typeof value === 'object' && value !== null) {
        translated[key] = await translateObject(value, targetLang);
      } else {
        translated[key] = value;
      }
    }
    return translated;
  };

  return { translateText, translateObject, isTranslating };
};