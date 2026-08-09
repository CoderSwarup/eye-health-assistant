import React from "react";

const roadmapItems = [
  {
    quarter: "Q3 2026",
    title: "Foundation",
    features: [
      "Timer mode with focus/break cycles",
      "Smart mode with camera-based blink estimation",
      "Guided eye exercises",
      "Educational content library",
    ],
  },
  {
    quarter: "Q4 2026",
    title: "Enhancement",
    features: [
      "Advanced analytics and insights",
      "Custom exercise creation",
      "Export and backup features",
      "Performance optimizations",
    ],
  },
  {
    quarter: "Q1 2027",
    title: "Expansion",
    features: [
      "Multi-language support",
      "Additional eye care content",
      "Community exercise sharing",
      "Integration with health apps",
    ],
  },
];

export function Roadmap() {
  return (
    <section className="py-20 px-4 bg-[var(--bg-primary)]">
      <div className="max-w-6xl mx-auto">
        <h2 className="text-3xl md:text-4xl font-bold text-center mb-4 text-[var(--text-primary)]">
          Roadmap
        </h2>
        <p className="text-center text-[var(--text-secondary)] mb-16 max-w-2xl mx-auto">
          Our journey to improve eye health for screen users everywhere.
        </p>

        <div className="grid md:grid-cols-3 gap-8">
          {roadmapItems.map((item) => (
            <div
              key={item.quarter}
              className="p-6 rounded-2xl bg-[var(--bg-secondary)] border border-[var(--border-primary)]"
            >
              <div className="text-sm font-semibold text-[var(--accent-primary)] mb-2">
                {item.quarter}
              </div>
              <h3 className="text-xl font-bold text-[var(--text-primary)] mb-4">
                {item.title}
              </h3>
              <ul className="space-y-3">
                {item.features.map((feature) => (
                  <li
                    key={feature}
                    className="flex items-start gap-3 text-[var(--text-secondary)]"
                  >
                    <span className="mt-1 w-2 h-2 rounded-full bg-[var(--accent-primary)] shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
