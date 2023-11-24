// components/Button.tsx

import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  label: string;
}

const baseClasses = 'text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline';

export const PrimaryButton: React.FC<ButtonProps> = ({ label, ...props }) => {
  return (
    <button
      {...props}
      className={`${baseClasses} bg-blue-500 hover:bg-blue-700 ${props.className}`}
    >
      {label}
    </button>
  );
};

export const SecondaryButton: React.FC<ButtonProps> = ({ label, ...props }) => {
  return (
    <button
      {...props}
      className={`${baseClasses} bg-gray-500 hover:bg-gray-700 ${props.className}`}
    >
      {label}
    </button>
  );
};
