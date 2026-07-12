import { navigation } from "../../constants/navigation";
import { NavLink } from "react-router-dom";
import { User } from "lucide-react";

export default function Sidebar() {
  return (
    <aside className="flex h-screen w-[280px] flex-col border-r border-gray-200 bg-white">
      {/* Header */}
      <div className="border-b border-gray-200 px-6 py-6">
        <h1 className="text-xl font-bold text-[#3D348B]">
          FluentPath AI
        </h1>

        <p className="text-sm text-gray-500">
          Personal English Coach
        </p>
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-2 p-4">
        {navigation.map((item) => {
          const Icon = item.icon;

          return (
            <NavLink
              key={item.title}
              to={item.path}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-xl px-4 py-3 transition ${
                  isActive
                    ? "bg-[#D0E6FF] text-[#3D348B] font-semibold"
                    : "text-gray-600 hover:bg-gray-100"
                }`
              }
            >
              <Icon size={20} />
              <span>{item.title}</span>
            </NavLink>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="border-t border-gray-200 p-5">
        <div className="flex items-center gap-3">
          <div className="flex h-11 w-11 items-center justify-center rounded-full bg-[#3D348B] text-white">
            <User size={20} />
          </div>

          <div>
            <h3 className="font-semibold text-[#4A4B4B]">
              Adeesha
            </h3>

            <p className="text-sm text-gray-500">
              Student
            </p>
          </div>
        </div>
      </div>
    </aside>
  );
}