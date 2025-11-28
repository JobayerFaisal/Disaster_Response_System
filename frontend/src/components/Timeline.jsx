export default function Timeline({ data }) {
  return (
    <div className="flex gap-2 mt-4">
      {Array.from({ length: 8 }).map((_, i) => {
        const active = data.some((d) => d.day >= i);
        return (
          <div
            key={i}
            className={`px-4 py-2 rounded text-center text-white ${
              active ? "bg-green-600" : "bg-gray-600"
            }`}
          >
            Day {i}
          </div>
        );
      })}
    </div>
  );
}
