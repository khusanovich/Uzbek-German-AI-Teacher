"use client";

import { useEffect, useState } from "react";
import type { Unit, CEFR } from "@/lib/types";
import { getUnits } from "@/lib/api";

interface UnitPickerProps {
  level: CEFR;
  selectedUnitId: string | null;
  onSelectUnit: (unit: Unit) => void;
}

export default function UnitPicker({
  level,
  selectedUnitId,
  onSelectUnit,
}: UnitPickerProps) {
  const [units, setUnits] = useState<Unit[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    setError(null);
    getUnits(level)
      .then((data) => {
        setUnits(data);
        if (data.length > 0 && !selectedUnitId) {
          onSelectUnit(data[0]);
        }
      })
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
  }, [level]);

  if (loading) {
    return (
      <div className="p-4 bg-white rounded-lg shadow">
        <p className="text-gray-500">Loading units...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 bg-red-50 rounded-lg border border-red-200">
        <p className="text-red-600">Error: {error}</p>
      </div>
    );
  }

  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h2 className="text-lg font-semibold mb-3">Select a Unit</h2>
      <div className="space-y-2">
        {units.map((unit) => (
          <button
            key={unit.id}
            onClick={() => onSelectUnit(unit)}
            className={`w-full text-left p-3 rounded-md transition-colors ${
              selectedUnitId === unit.id
                ? "bg-blue-500 text-white"
                : "bg-gray-100 hover:bg-gray-200 text-gray-900"
            }`}
          >
            <div className="font-medium">{unit.title}</div>
            <div
              className={`text-sm mt-1 ${
                selectedUnitId === unit.id ? "text-blue-100" : "text-gray-600"
              }`}
            >
              {unit.objectives.slice(0, 2).join(" • ")}
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
