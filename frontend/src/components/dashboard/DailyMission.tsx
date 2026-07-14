import type { DailyMission } from "../../types/dashboard";

interface Props {
  missions: DailyMission[];
}

export default function DailyMission({ missions }: Props) {
  return (
    <div className="rounded-3xl bg-white p-6 shadow-sm">
      <h2 className="mb-6 text-xl font-bold text-[#3D348B]">
        Daily Mission
      </h2>

      <div className="space-y-5">
        {missions.map((mission) => (
          <div key={mission.skill}>
            <div className="flex justify-between mb-2">
              <span>{mission.skill}</span>

              <span>
                {mission.completed} / {mission.target}
              </span>
            </div>

            <div className="h-2 rounded-full bg-gray-200">
              <div
                className="h-2 rounded-full bg-blue-500"
                style={{
                  width: `${(mission.completed / mission.target) * 100}%`,
                }}
              />
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}