class StudyOutcome:
    def __init__(self, initial_penalty: int, mean: float, ba_ma: bool, lecture: int, research_group: int,
                 research_paper: int,
                 other_pillars: list, previous_internship: bool, previous_paper: bool, tdk: bool, last_semester: bool,
                 on_time: bool,
                 passive_limit: bool, package: bool, assembly: bool, prof_day: bool):
        # first
        self.initial_penalty = initial_penalty
        self.mean = mean
        self.is_bachelor = ba_ma
        # second
        self.lecture = lecture
        self.research_group = research_group
        self.research_paper = research_paper
        self.other_pillars = other_pillars
        self.previous_internship = previous_internship
        # third
        self.previous_paper = previous_paper
        self.tdk = tdk
        self.last_semester = last_semester
        self.on_time = on_time
        # fourth
        self.passive_limit = passive_limit
        self.package = package
        self.assembly = assembly
        self.prof_day = prof_day
        # calculated
        self.secretary_pillar = 0
        self.internship_pillar = 0
        self.all_pillar_points = 0
        self.achieved_pillars = 0
        self.overall_points = 0
        self.calculated_points = dict()  # intermediate dict
        self.final_points = dict()
        self.failure = dict()
        self.result = dict()

    def calculate_is_drop_out(self):
        fail_dict = {
            "Tanulmányait várhatóan időben befejezi?": self.on_time,  # 18. § 1a-b
            "Egyetemi hallgatói jogviszonyát maximum kétszer szüneteltette?": self.passive_limit,  # 18. § 1c
            "Büntetőpontok száma kevesebb mint három?": self.overall_points < 3,  # 18. § 1d
            "Legalább egy pillért teljesített a félév során?": self.achieved_pillars > 0  # 18. § 1e
        }
        drop_out = not all(fail_dict.values())
        self.failure["overall"] = drop_out
        self.failure.update(fail_dict)

    def calculate_admin_points(self):
        self.calculated_points.update({
            "Egyetemi ösztöndíj átlaga eléri a 4.0-át?": 0 if self.mean else 1,  # 16. § A
            "Kari TDK konferencián bekerült-e az első négy közé nem szak/évfolyam dolgozattal?": -1 if self.tdk else 0,
            # 6. § 10-11
            "Időben benyújtottad a szakmai pakkot az adott félévben?": 0 if self.package else 1,  # 16. § c
            "Részt vettél a műhelyülésen az adott félévben, vagy igazolta-e a hiányzását?": 0 if self.assembly else 1,
            # 16. § d
            "Részt vett-e a szakmai napokon hallgatóságként az adott félévben vagy igazolta-e hiányzását?": 0 if self.prof_day else 1
            # 16. § b

        })

    def research_paper_penalty(self):
        if self.last_semester and not self.previous_paper and self.research_paper == 0:
            penalty_point = 2  # 10. § 11, 17. §
            self.calculated_points.update({
                "Az adott képzésen nem teljesített tutori pillért.": penalty_point
            })

    def master_internship_penalty(self):
        if not self.is_bachelor and not self.previous_internship and "internship" not in self.other_pillars:
            penalty_point = 1  # 11. § 8, 16. § f
            self.calculated_points.update({
                "Sem mesterképzése alatt, sem korábban nem teljesített szakmai gyakorlatot.": penalty_point
            })

    def no_lecture_pillar_penalty(self):
        if self.lecture == 0:
            penalty_point = 1  # 16. § e
            self.calculated_points.update({
                "Teljesített pillérei között nem szerepel kurzus": penalty_point
            })

    def points_for_pillars(self):
        msg = "Pillér pontok"
        penalty_point = 0
        if self.achieved_pillars == 0:
            penalty_point = 2
        elif self.achieved_pillars == 1:
            penalty_point = 1  # 16. § e
        elif self.achieved_pillars == 2:
            penalty_point = 0
        elif self.achieved_pillars == 3:
            penalty_point = -1
        elif self.achieved_pillars >= 4:
            penalty_point = -2
        self.calculated_points.update({
            msg: penalty_point
        })

    def calculate_achieved_pillars(self):
        self.internship_pillar = -1 if not self.previous_internship and "internship" in self.other_pillars else 0  # 11. § 8, 16. § f
        self.achieved_pillars = sum([abs(self.internship_pillar), self.lecture, self.research_group, self.research_paper])
        if 2 <= self.achieved_pillars < 4 and "secretary" in self.other_pillars:
            self.achieved_pillars += 1  # 5. § 5

    def calculate_score_dict(self):
        msg = "Pillér pontok"
        self.calculate_achieved_pillars()
        self.calculate_admin_points()
        self.research_paper_penalty()
        self.master_internship_penalty()
        self.no_lecture_pillar_penalty()
        self.points_for_pillars()
        self.final_points = {item: point for item, point in self.calculated_points.items() if point != 0 and item != msg}
        self.overall_points = self.initial_penalty + sum(self.final_points.values())

    def calculate_overall_performance(self):
        self.calculate_score_dict()
        self.calculate_is_drop_out()
        self.result = {
            'score': {
                "total": self.overall_points,
                **self.final_points
            },
            'failure': self.failure
        }
        return self.result


if __name__ == "__main__":
    example = {'passive_limit': False, 'package': True, 'assembly': True, 'prof_day': True,
               'previous_paper': False, 'tdk': True, 'last_semester': False, 'on_time': True, 'lecture': 0,
               'research_group': 0, 'research_paper': 0, 'other_pillars': ['internship', 'secretary'],
               'previous_internship': False,
               'initial_penalty': 0, 'mean': 4.0, 'ba_ma': False}
    outcome_object = StudyOutcome(**example)
    outcome_result = outcome_object.calculate_overall_performance()
    print(outcome_result)
