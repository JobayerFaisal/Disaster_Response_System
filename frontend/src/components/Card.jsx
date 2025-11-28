import React from "react";


interface Props {
  title: string;
  value?: string | number;
  children?: React.ReactNode;
}

export default function Card({ title, value, children }: Props) {
  return (
    <div className="bg-white shadow rounded p-4 border">
      <h2 className="text-lg font-semibold">{title}</h2>
      {value && <p className="text-2xl font-bold mt-2">{value}</p>}
      {children}
    </div>
  );
}
