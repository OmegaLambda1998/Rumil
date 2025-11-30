from rumil.templates.template import Template
from typing import TYPE_CHECKING
from dataclasses import dataclass, field

if TYPE_CHECKING:
    from rumil.notes import Note


@dataclass
class Medication:
    name: str
    week: int
    remaining: int
    repeats: int
    weekly: float = field(init=False)
    weeks_left: int = field(init=False)
    morning: float = 0
    noon: float = 0
    evening: float = 0
    night: float = 0
    per_day: bool = True

    def __post_init__(self):
        self.weekly = (7 if self.per_day else 1) * (
            self.morning + self.noon + self.evening + self.night
        )
        self.weeks_left = int(self.remaining / self.weekly)

        self.weeks_left -= self.week
        self.remaining -= int(self.weekly * self.week)


class Medications(Template):
    id = "medications"
    order = 1

    def __init__(self, *args, week: int, medication: list[dict], **kwargs):
        super().__init__(*args, **kwargs)
        self.medications: list[Medication] = []
        for med in medication:
            self.medications.append(Medication(week=week, **med))

    def apply_to(self, note: "Note"):
        super().apply_to(note)

        note.markdown += "\n\n## Summary"

        table_head = "\n| Name | Morn | Noon | Eve | Bed | Weekly | Remaining | Weeks Left | Repeats |"
        table_div = "|---|---|---|---|---|--:|--:|--:|--:|"
        table_rows = [table_head, table_div]
        for med in self.medications:
            weeks_left = str(med.weeks_left)
            if med.weeks_left < 3:
                weeks_left = f"*{weeks_left}*"
            if med.weeks_left < 2:
                weeks_left = f"*{weeks_left}*"
            if med.weeks_left < 1:
                weeks_left = f"*{weeks_left}*"

            repeats = str(med.repeats)
            if med.repeats < 3:
                repeats = f"*{repeats}*"
            if med.repeats < 2:
                repeats = f"*{repeats}*"
            if med.repeats < 1:
                repeats = f"*{repeats}*"
            if med.repeats < 0:
                repeats = "-"

            table_row = f"| {med.name} | {'-' if med.morning == 0 else med.morning} | {'-' if med.noon == 0 else med.noon} | {'-' if med.evening == 0 else med.evening} | {'-' if med.night == 0 else med.night} | {med.weekly} | {med.remaining} | {weeks_left} | {repeats} |"
            table_rows.append(table_row)
        table = "\n".join(table_rows) + "\n"
        note.markdown += table

        note.markdown += "\n\n## Restock\n"
        for med in self.medications:
            if med.weeks_left < 3:
                name = med.name
                symbol = "."
                if med.weeks_left < 2:
                    symbol = "!"
                if med.weeks_left < 1:
                    name = f"*{name}*"
                note.markdown += f"\n- [{symbol}] {name}"

        note.markdown += "\n\n## Renew\n"
        for med in self.medications:
            if med.repeats < 0:
                continue
            if med.repeats < 3:
                name = med.name
                symbol = "."
                if med.repeats < 2:
                    symbol = "!"
                if med.repeats < 1:
                    name = f"*{name}*"
                note.markdown += f"\n- [{symbol}] {name}"


Medications.register()
