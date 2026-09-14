"use client";

import { useEffect, useState } from "react";

export default function ThemeToggle() {
  const [theme, setTheme] = useState("system");

  useEffect(() => {
    const saved = window.localStorage.getItem("kb-theme") || "system";
    setTheme(saved);
    document.documentElement.dataset.theme = saved;
  }, []);

  function toggle() {
    const next = theme === "dark" ? "light" : "dark";
    setTheme(next);
    window.localStorage.setItem("kb-theme", next);
    document.documentElement.dataset.theme = next;
  }

  return (
    <button className="icon-button" onClick={toggle} aria-label="切换深浅色">
      {theme === "dark" ? "☀" : "◐"}
    </button>
  );
}
