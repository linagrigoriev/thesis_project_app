import React, { useState, useEffect } from "react";
import "./App.css";

function TimetableComponent({ data }) {
  const [hoveredSlot, setHoveredSlot] = useState(null);

  const handleSlotHover = (dayIndex, slotIndex, label) => {
    setHoveredSlot({ dayIndex, slotIndex, label });
  };

  const handleSlotLeave = () => {
    setHoveredSlot(null);
  };

  const getTimeSlotLabel = (index) => {
    const startHour = 8 + index * 2;
    const endHour = startHour + 2;
    return `${startHour}:00 - ${endHour}:00`;
  };

  return (
    <div className="timetable">
      <div className="day-container">
        <table className="timetable-table">
          <thead>
            <tr>
              <th className="timeslot-header">Ora</th>
              {data.map((day, index) => (
                <th key={index} className="day-header">
                  {day.label}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {data[0].slots.map((slot, slotIndex) => (
              <tr key={slotIndex}>
                <td className="time-slot">
                  <p>{getTimeSlotLabel(slotIndex)}</p>
                </td>
                {data.map((day, dayIndex) => {
                  const currentSlot = day.slots[slotIndex];
                  if (!currentSlot) {
                    return <td key={dayIndex} className="day"></td>;
                  }
                  return (
                    <td key={dayIndex} className="day">
                      {currentSlot.map((slot, index) => (
                        <div
                          key={index}
                          className="time-slot slot-with-label"
                          style={{
                            backgroundColor: slot.color,
                            position: "relative",
                            width: "150px",
                            height: "wrap-content",
                          }}
                          onMouseEnter={() =>
                            handleSlotHover(dayIndex, slotIndex, slot.label)
                          }
                          onMouseLeave={handleSlotLeave}
                        >
                          {slot.label && (
                            <>
                              {slot.group_subgroup_number === "0"
                                ? `${slot.label}, curs, ${slot.room_name}, ${slot.study_program_name}`
                                : slot.seminar_laboratory === "S"
                                ? `${slot.label}, sem, ${slot.room_name}, ${slot.study_program_name}, gr ${slot.group_subgroup_number}`
                                : `${slot.label}, lab, ${slot.room_name}, ${slot.study_program_name}, sem ${slot.group_subgroup_number}`}
                              {hoveredSlot &&
                                hoveredSlot.dayIndex === dayIndex &&
                                hoveredSlot.slotIndex === slotIndex &&
                                hoveredSlot.label === slot.label && (
                                  <div className="additional-info">
                                    {slot.group_subgroup_number === "0"
                                      ? `Curs: ${slot.course_name}, Cadrul didactic: ${slot.professor}, 
                                      Specializare: ${slot.study_program_name}`
                                          .split(", ")
                                          .map((line, index) => (
                                            <React.Fragment key={index}>
                                              {line}
                                              <br />
                                            </React.Fragment>
                                          ))
                                      : slot.seminar_laboratory === "S"
                                      ? `Seminar: ${slot.course_name}, Cadrul didactic: ${slot.professor}, 
                                        Specializare: ${slot.study_program_name}, Grupa: ${slot.group_subgroup_number}`
                                          .split(", ")
                                          .map((line, index) => (
                                            <React.Fragment key={index}>
                                              {line}
                                              <br />
                                            </React.Fragment>
                                          ))
                                      : `Laborator:, ${slot.course_name}, ${slot.professor}, 
                                        Specializare: ${slot.study_program_name}, Semigrupa: ${slot.group_subgroup_number}`
                                          .split(", ")
                                          .map((line, index) => (
                                            <React.Fragment key={index}>
                                              {line}
                                              <br />
                                            </React.Fragment>
                                          ))}
                                  </div>
                                )}
                            </>
                          )}
                        </div>
                      ))}
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function App() {
  const [selectedAlgorithm, setSelectedAlgorithm] = useState("");
  const [selectedOption, setSelectedOption] = useState("");
  const [selectedId, setSelectedId] = useState("");
  const [professors, setProfessors] = useState([]);
  const [studyPrograms, setStudyPrograms] = useState([]);
  const [rooms, setRooms] = useState([]);
  const [timetableData, setTimetableData] = useState(null);
  const [showTimetable, setShowTimetable] = useState(false);

  const handleAlgorithmChange = (event) => {
    setSelectedAlgorithm(event.target.value);
  };

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value);
    setSelectedId("");
    setShowTimetable(false);
  };

  const handleIdChange = (event) => {
    setSelectedId(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!selectedId || !selectedAlgorithm) {
      alert("Vă rugăm să selectați o opțiune și un algoritm");
      return;
    }

    try {
      let data_json = {};
      if (selectedOption === "2") {
        const response = await fetch(
          `/generate_plot_room?choice_id=${selectedId}`
        );
        if (!response.ok) {
          throw new Error("Nu s-au putut prelua datele orarului");
        }
        data_json = await response.json();
      } else if (selectedOption === "1") {
        const response = await fetch(
          `/generate_plot_professor?choice_id=${selectedId}`
        );
        if (!response.ok) {
          throw new Error("Nu s-au putut prelua datele orarului");
        }
        data_json = await response.json();
      } else if (selectedOption === "0") {
        const response = await fetch(
          `/generate_plot_study_program?choice_id=${selectedId}`
        );
        if (!response.ok) {
          throw new Error("Nu s-au putut prelua datele orarului");
        }
        data_json = await response.json();
      }

      if (!Array.isArray(data_json)) {
        throw new Error("Datele nu sunt în formatul așteptat");
      }

      const groupColors = {
        0: "#2C7DA0",
        L: "#01497C",
        S: "#012A4A",
      };

      const days = [
        { id: "1", day_name: "Luni" },
        { id: "2", day_name: "Marti" },
        { id: "3", day_name: "Miercuri" },
        { id: "4", day_name: "Joi" },
        { id: "5", day_name: "Vineri" },
      ];

      const timetable = days.map((day) => {
        return {
          label: day.day_name,
          slots: [...Array(6).keys()].map((i) => {
            const timeslotId = (i + 1).toString();
            const slotSolution = data_json.filter(
              (item) =>
                item.timeslot_id === timeslotId &&
                item.day_name === day.day_name
            );
            if (slotSolution.length === 0) {
              return [
                {
                  label: "",
                  color: "transparent",
                },
              ];
            } else {
              return slotSolution.map((solution) => {
                const courseName = solution.course_name;
                const lecturerName = solution.professor_name;
                const groupSubgroupNumber = solution.group_subgroup_number;
                const shortName = solution.short_name;
                const color =
                  groupColors[
                    groupSubgroupNumber === "0"
                      ? "0"
                      : solution.seminar_laboratory
                  ];
                const seminarLaboratory = solution.seminar_laboratory;
                const roomName = solution.room_name;
                const studyProgramName = solution.study_program_name;
                return {
                  label: shortName,
                  course_name: courseName,
                  professor: lecturerName,
                  group_subgroup_number: groupSubgroupNumber,
                  color: color,
                  seminar_laboratory: seminarLaboratory,
                  room_name: roomName,
                  study_program_name: studyProgramName,
                };
              });
            }
          }),
        };
      });

      setTimetableData(timetable);
      setShowTimetable(true);
    } catch (error) {
      console.error("Eroare:", error.message);
    }
  };

  useEffect(() => {
    if (selectedAlgorithm === "CSP") {
      fetch("/CSP_algorithm", { method: "POST" })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Răspunsul rețelei nu a fost ok");
          }
        })
        .catch((error) => {
          console.error("Eroare la preluarea soluției CSP:", error);
        });
    } else if (selectedAlgorithm === "GA") {
      fetch("/genetic_algorithm", { method: "POST" })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Răspunsul rețelei nu a fost ok");
          }
        })
        .catch((error) => {
          console.error("Eroare la preluarea soluției GA:", error);
        });
    }
  }, [selectedAlgorithm]);

  useEffect(() => {
    if (selectedOption === "1") {
      fetch("/professors")
        .then((res) => res.json())
        .then((data) => {
          setProfessors(data.professors);
        })
        .catch((error) => {
          console.error("Eroare la preluarea profesorilor:", error);
        });
    } else if (selectedOption === "0") {
      fetch("/study_programs")
        .then((res) => res.json())
        .then((data) => {
          setStudyPrograms(data.study_programs);
        })
        .catch((error) => {
          console.error("Eroare la preluarea specializărilor:", error);
        });
    } else if (selectedOption === "2") {
      fetch("/rooms")
        .then((res) => res.json())
        .then((data) => {
          setRooms(data.rooms);
        })
        .catch((error) => {
          console.error("Eroare la preluarea sălilor:", error);
        });
    }
  }, [selectedOption]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Generarea Orarului Universitar</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>
              Alegeți algoritmul:
              <select
                value={selectedAlgorithm}
                onChange={handleAlgorithmChange}
              >
                <option value="">Selectați...</option>
                <option value="CSP">Algoritmul CSP</option>
                <option value="GA">Algoritmul Genetic</option>
              </select>
            </label>
          </div>
          <div>
            <label>
              Ajegeți o opțiune:
              <select value={selectedOption} onChange={handleOptionChange}>
                <option value="">Selectați...</option>
                <option value="1">Profesor</option>
                <option value="0">Specializare</option>
                <option value="2">Sală</option>
              </select>
            </label>
          </div>
          {selectedOption === "1" && (
            <div>
              <label>Alegeți Profesorul:</label>
              <select value={selectedId} onChange={handleIdChange}>
                <option value="">Selectați...</option>
                {professors.map((professor, index) => (
                  <option key={index} value={professor}>
                    {professor}
                  </option>
                ))}
              </select>
            </div>
          )}
          {selectedOption === "0" && (
            <div>
              <label>Alegeți Specializarea:</label>
              <select value={selectedId} onChange={handleIdChange}>
                <option value="">Selectați...</option>
                {studyPrograms.map((study_program, index) => (
                  <option key={index} value={study_program}>
                    {study_program}
                  </option>
                ))}
              </select>
            </div>
          )}
          {selectedOption === "2" && (
            <div>
              <label>Alegeți Sala:</label>
              <select value={selectedId} onChange={handleIdChange}>
                <option value="">Selectați...</option>
                {rooms.map((room, index) => (
                  <option key={index} value={room}>
                    {room}
                  </option>
                ))}
              </select>
            </div>
          )}
          <button type="submit">Generarea Orarului</button>
        </form>
        {showTimetable && timetableData && (
          <TimetableComponent data={timetableData} />
        )}
      </header>
    </div>
  );
}

export default App;
