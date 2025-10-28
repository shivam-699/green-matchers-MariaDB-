import { useEffect } from 'react';

const Toast = ({ message, type = 'info', onClose }) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onClose?.();
    }, 4000);

    return () => clearTimeout(timer);
  }, [onClose]);

  const typeConfig = {
    success: {
      bg: 'bg-emerald-500/20',
      border: 'border-emerald-500/50',
      text: 'text-emerald-300',
      icon: '✅',
      iconBg: 'bg-emerald-500/20',
      progressBg: 'bg-emerald-500',
    },
    error: {
      bg: 'bg-red-500/20',
      border: 'border-red-500/50',
      text: 'text-red-300',
      icon: '❌',
      iconBg: 'bg-red-500/20',
      progressBg: 'bg-red-500',
    },
    warning: {
      bg: 'bg-yellow-500/20',
      border: 'border-yellow-500/50',
      text: 'text-yellow-300',
      icon: '⚠️',
      iconBg: 'bg-yellow-500/20',
      progressBg: 'bg-yellow-500',
    },
    info: {
      bg: 'bg-blue-500/20',
      border: 'border-blue-500/50',
      text: 'text-blue-300',
      icon: 'ℹ️',
      iconBg: 'bg-blue-500/20',
      progressBg: 'bg-blue-500',
    },
  };

  const config = typeConfig[type] || typeConfig.info;

  return (
    <>
      <style>{`
        @keyframes slide-in {
          from {
            opacity: 0;
            transform: translateX(100%);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        @keyframes progress {
          from {
            width: 100%;
          }
          to {
            width: 0%;
          }
        }
        
        .animate-slide-in {
          animation: slide-in 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }

        .animate-progress {
          animation: progress 4s linear forwards;
        }
      `}</style>

      <div className="fixed top-6 right-6 z-50 animate-slide-in">
        <div 
          className={`${config.bg} ${config.border} backdrop-blur-xl border rounded-2xl shadow-2xl overflow-hidden min-w-[320px] max-w-md`}
        >
          <div className="flex items-start gap-4 p-4">
            {/* Icon */}
            <div className={`${config.iconBg} p-2 rounded-xl flex-shrink-0 text-2xl`}>
              {config.icon}
            </div>

            {/* Message */}
            <div className="flex-1 pt-1">
              <p className={`${config.text} font-medium leading-relaxed`}>
                {message}
              </p>
            </div>

            {/* Close Button */}
            <button
              onClick={onClose}
              className={`${config.text} hover:opacity-70 transition-opacity p-1 flex-shrink-0 text-xl leading-none`}
              aria-label="Close notification"
            >
              ✕
            </button>
          </div>

          {/* Progress Bar */}
          <div className="h-1 bg-white/10">
            <div className={`h-full ${config.progressBg} animate-progress`} />
          </div>
        </div>
      </div>
    </>
  );
};

export default Toast;