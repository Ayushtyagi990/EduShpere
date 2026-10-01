import { useState } from "react";

const alertStyles = {
  success: {
    container: "bg-emerald-50 text-emerald-800 border-emerald-200",
    icon: (
      <svg
        className="w-5 h-5 text-emerald-500 shrink-0"
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path
          fillRule="evenodd"
          d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
          clipRule="evenodd"
        />
      </svg>
    ),
    closeBtn: "text-emerald-500 hover:bg-emerald-100 focus:ring-emerald-400",
  },
  danger: {
    container: "bg-rose-50 text-rose-800 border-rose-200",
    icon: (
      <svg
        className="w-5 h-5 text-rose-500 shrink-0"
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path
          fillRule="evenodd"
          d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
          clipRule="evenodd"
        />
      </svg>
    ),
    closeBtn: "text-rose-500 hover:bg-rose-100 focus:ring-rose-400",
  },
  warning: {
    container: "bg-amber-50 text-amber-800 border-amber-200",
    icon: (
      <svg
        className="w-5 h-5 text-amber-500 shrink-0"
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path
          fillRule="evenodd"
          d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
          clipRule="evenodd"
        />
      </svg>
    ),
    closeBtn: "text-amber-500 hover:bg-amber-100 focus:ring-amber-400",
  },
  info: {
    container: "bg-sky-50 text-sky-800 border-sky-200",
    icon: (
      <svg
        className="w-5 h-5 text-sky-500 shrink-0"
        fill="currentColor"
        viewBox="0 0 20 20"
      >
        <path
          fillRule="evenodd"
          d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
          clipRule="evenodd"
        />
      </svg>
    ),
    closeBtn: "text-sky-500 hover:bg-sky-100 focus:ring-sky-400",
  },
};

export const Alert = ({ type = "info", title, message, onClose }) => {
  const [isVisible, setIsVisible] = useState(true);
  const [isDismissing, setIsDismissing] = useState(false);

  const handleClose = () => {
    setIsDismissing(true);
    setTimeout(() => {
      setIsVisible(false);
      if (onClose) onClose();
    }, 300);
  };

  if (!isVisible) return null;

  const style = alertStyles[type] || alertStyles.info;

  return (
    <div
      role="alert"
      className={`flex items-start gap-3 p-4 border rounded-xl shadow-sm transition-all duration-300 ease-in-out ${
        style.container
      } ${
        isDismissing
          ? "opacity-0 -translate-y-2 scale-95"
          : "opacity-100 translate-y-0 scale-100"
      }`}
    >
      {/* Icon */}
      <div className="mt-0.5">{style.icon}</div>

      {/* Content */}
      <div className="flex-1 text-sm">
        {title && <h4 className="font-semibold mb-0.5">{title}</h4>}
        <p className="leading-relaxed">{message}</p>
      </div>

      {/* Close Button */}
      <button
        type="button"
        onClick={handleClose}
        aria-label="Close alert"
        className={`p-1.5 -mr-1 -mt-1 inline-flex rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-offset-1 ${style.closeBtn}`}
      >
        <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
          <path
            fillRule="evenodd"
            d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
            clipRule="evenodd"
          />
        </svg>
      </button>
    </div>
  );
};
