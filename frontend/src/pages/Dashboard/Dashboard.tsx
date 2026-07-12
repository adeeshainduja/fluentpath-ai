import { useDashboard } from "../../hooks/useDashboard";

export default function Dashboard() {
  const { data, isLoading, error } = useDashboard(1);

  if (isLoading) return <h1>Loading...</h1>;

  if (error) return <h1>Error loading dashboard.</h1>;

  return (
    <pre>{JSON.stringify(data, null, 2)}</pre>
  );
}