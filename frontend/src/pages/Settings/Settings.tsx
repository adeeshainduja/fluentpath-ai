import {
  Bell,
  Download,
  Languages,
  LogOut,
  Mic,
  Shield,
} from "lucide-react";
import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useLearnerIntelligence } from "../../hooks/useLearnerIntelligence";

const learnerId = 1;

export default function Settings() {
  const navigate = useNavigate();
  const { data } = useLearnerIntelligence(learnerId);
  const [dailyReminder, setDailyReminder] = useState(true);
  const [weeklySummary, setWeeklySummary] = useState(true);
  const [microphoneEnabled, setMicrophoneEnabled] =
    useState(true);
  const [noiseReduction, setNoiseReduction] = useState(true);
  const [language, setLanguage] = useState("English");
  const [theme, setTheme] = useState("System");

  const exportLearnerData = () => {
    if (!data) {
      return;
    }

    const file = new Blob(
      [
        JSON.stringify(
          data,
          null,
          2
        ),
      ],
      {
        type: "application/json",
      }
    );
    const url = URL.createObjectURL(file);
    const link = document.createElement("a");

    link.href = url;
    link.download = `fluentpath-learner-${learnerId}.json`;
    link.click();
    URL.revokeObjectURL(url);
  };

  const signOut = () => {
    localStorage.clear();
    sessionStorage.clear();
    navigate("/");
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-4xl font-bold text-[#3D348B]">
          Settings
        </h1>
        <p className="text-gray-500">
          Preferences for learning, notifications, audio, and data.
        </p>
      </div>

      <section className="grid grid-cols-1 gap-8 xl:grid-cols-2">
        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <Bell className="text-[#3D348B]" size={24} />
            <h2 className="text-xl font-bold text-[#3D348B]">
              Notifications
            </h2>
          </div>

          <div className="mt-5 space-y-4">
            <label className="flex items-center justify-between gap-4 rounded-xl bg-[#F5F6FC] px-4 py-3">
              <span>
                <span className="block font-semibold text-[#4A4B4B]">
                  Daily practice reminder
                </span>
                <span className="text-sm text-gray-500">
                  Prompt a short daily learning session.
                </span>
              </span>
              <input
                checked={dailyReminder}
                className="h-5 w-5 accent-[#3D348B]"
                type="checkbox"
                onChange={(event) =>
                  setDailyReminder(event.target.checked)
                }
              />
            </label>

            <label className="flex items-center justify-between gap-4 rounded-xl bg-[#F5F6FC] px-4 py-3">
              <span>
                <span className="block font-semibold text-[#4A4B4B]">
                  Weekly progress summary
                </span>
                <span className="text-sm text-gray-500">
                  Receive a compact review of progress.
                </span>
              </span>
              <input
                checked={weeklySummary}
                className="h-5 w-5 accent-[#3D348B]"
                type="checkbox"
                onChange={(event) =>
                  setWeeklySummary(event.target.checked)
                }
              />
            </label>
          </div>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <Languages className="text-[#3D348B]" size={24} />
            <h2 className="text-xl font-bold text-[#3D348B]">
              Language & Theme
            </h2>
          </div>

          <div className="mt-5 grid grid-cols-1 gap-4 md:grid-cols-2">
            <label className="space-y-2">
              <span className="text-sm font-semibold text-gray-500">
                Interface language
              </span>
              <select
                className="w-full rounded-xl border border-gray-200 bg-[#F5F6FC] px-4 py-3 text-[#4A4B4B]"
                value={language}
                onChange={(event) =>
                  setLanguage(event.target.value)
                }
              >
                <option>English</option>
              </select>
            </label>

            <label className="space-y-2">
              <span className="text-sm font-semibold text-gray-500">
                Theme
              </span>
              <select
                className="w-full rounded-xl border border-gray-200 bg-[#F5F6FC] px-4 py-3 text-[#4A4B4B]"
                value={theme}
                onChange={(event) =>
                  setTheme(event.target.value)
                }
              >
                <option>System</option>
                <option>Light</option>
                <option>Dark</option>
              </select>
            </label>
          </div>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <Mic className="text-[#3D348B]" size={24} />
            <h2 className="text-xl font-bold text-[#3D348B]">
              Microphone
            </h2>
          </div>

          <div className="mt-5 space-y-4">
            <label className="flex items-center justify-between gap-4 rounded-xl bg-[#F5F6FC] px-4 py-3">
              <span className="font-semibold text-[#4A4B4B]">
                Enable microphone practice
              </span>
              <input
                checked={microphoneEnabled}
                className="h-5 w-5 accent-[#3D348B]"
                type="checkbox"
                onChange={(event) =>
                  setMicrophoneEnabled(event.target.checked)
                }
              />
            </label>

            <label className="flex items-center justify-between gap-4 rounded-xl bg-[#F5F6FC] px-4 py-3">
              <span className="font-semibold text-[#4A4B4B]">
                Noise reduction
              </span>
              <input
                checked={noiseReduction}
                className="h-5 w-5 accent-[#3D348B]"
                type="checkbox"
                onChange={(event) =>
                  setNoiseReduction(event.target.checked)
                }
              />
            </label>
          </div>
        </div>

        <div className="rounded-2xl bg-white p-6 shadow-sm">
          <div className="flex items-center gap-3">
            <Shield className="text-[#3D348B]" size={24} />
            <h2 className="text-xl font-bold text-[#3D348B]">
              Data & Account
            </h2>
          </div>

          <div className="mt-5 space-y-4">
            <button
              className="flex w-full items-center justify-between rounded-xl bg-[#F5F6FC] px-4 py-3 text-left font-semibold text-[#4A4B4B] transition hover:bg-[#D0E6FF]"
              type="button"
              onClick={exportLearnerData}
            >
              <span className="flex items-center gap-3">
                <Download size={18} />
                Export learner data
              </span>
            </button>

            <button
              className="flex w-full items-center justify-between rounded-xl bg-red-50 px-4 py-3 text-left font-semibold text-red-600"
              type="button"
              onClick={signOut}
            >
              <span className="flex items-center gap-3">
                <LogOut size={18} />
                Sign out
              </span>
            </button>
          </div>
        </div>
      </section>
    </div>
  );
}
