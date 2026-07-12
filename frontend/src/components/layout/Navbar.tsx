import { Bell, Search } from "lucide-react";

export default function Navbar() {
  return (
    <header className="flex h-20 items-center justify-between border-b border-gray-200 bg-white px-8">
      {/* Left */}
      <div>
        <h1 className="text-2xl font-bold text-[#3D348B]">
          Dashboard
        </h1>

        <p className="text-sm text-gray-500">
          Welcome back 👋
        </p>
      </div>

      {/* Right */}
      <div className="flex items-center gap-5">
        {/* Search */}
        <div className="flex items-center gap-2 rounded-xl bg-[#F5F6FC] px-4 py-2">
          <Search size={18} className="text-gray-400" />

          <input
            type="text"
            placeholder="Search..."
            className="bg-transparent outline-none"
          />
        </div>

        {/* Notification */}
        <button className="rounded-xl bg-[#F5F6FC] p-3 transition hover:bg-[#D0E6FF]">
          <Bell size={20} className="text-[#3D348B]" />
        </button>

        {/* Avatar */}
        <img
          src="https://ui-avatars.com/api/?name=Adeesha"
          alt="User"
          className="h-11 w-11 rounded-full"
        />
      </div>
    </header>
  );
}