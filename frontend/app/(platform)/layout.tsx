import Link from "next/link";

const NAV = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/honey-companies", label: "NZ Honey Companies" },
  { href: "/buyers", label: "Indian Buyers" },
  { href: "/intelligence", label: "Intelligence" },
  { href: "/pipeline", label: "Pipeline" },
];

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">Solutionists</div>
        <nav>
          {NAV.map((item) => (
            <Link key={item.href} href={item.href}>
              {item.label}
            </Link>
          ))}
        </nav>
      </aside>
      <main className="main">{children}</main>
    </div>
  );
}
