"""
Comprehensive seed command for TMS test data.
Run: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from datetime import date, time, timedelta
import bcrypt


def make_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


class Command(BaseCommand):
    help = 'Seed the database with diverse test data for all features'

    def handle(self, *args, **options):
        self.stdout.write(self.style.WARNING('⏳  Seeding test data...'))
        with transaction.atomic():
            self._seed_all()
        self.stdout.write(self.style.SUCCESS('✅  Seeding complete!'))
        self._print_credentials()

    # ─────────────────────────────────────────────
    def _seed_all(self):
        from timetable.models import (
            University, Branch, College, Department, CollegeDepartment,
            AcademicYear, DepartmentAcademicPeriod, DepartmentStudentSettings,
            Specialization, Course, Room, Hall, CollegeRoom, CollegeHall,
            Professor, ProfessorCollegeRelation, Student, Role,
            LectureSchedule, LabSchedule, AlternativeTime, TaughtLecture,
            Notification, ScheduleDeadline, ScheduleChangeLog, UnifiedUser,
        )

        # ── 1. University & Branches ─────────────────
        uni, _ = University.objects.get_or_create(
            name='جامعة السودان للعلوم والتكنولوجيا',
            defaults={'code': 'SUST', 'established_year': 1975}
        )
        branch_main, _ = Branch.objects.get_or_create(
            university=uni, name='الفرع الرئيسي - الخرطوم', defaults={'is_main': True}
        )
        branch_north, _ = Branch.objects.get_or_create(
            university=uni, name='فرع بحري', defaults={'is_main': False}
        )
        branch_east, _ = Branch.objects.get_or_create(
            university=uni, name='فرع شرق النيل', defaults={'is_main': False}
        )

        # ── 2. Colleges ──────────────────────────────
        col_eng, _ = College.objects.get_or_create(
            name='كلية الهندسة', defaults={'branch': branch_main, 'code': 'ENG'}
        )
        col_cs, _ = College.objects.get_or_create(
            name='كلية علوم الحاسوب والتقنية', defaults={'branch': branch_main, 'code': 'CS'}
        )
        col_sci, _ = College.objects.get_or_create(
            name='كلية العلوم', defaults={'branch': branch_north, 'code': 'SCI'}
        )
        col_bus, _ = College.objects.get_or_create(
            name='كلية إدارة الأعمال', defaults={'branch': branch_east, 'code': 'BUS'}
        )
        colleges = [col_eng, col_cs, col_sci, col_bus]

        # ── 3. Departments ───────────────────────────
        dept_civil, _ = Department.objects.get_or_create(
            name='قسم الهندسة المدنية',
            defaults={'program_type': 'بكالوريوس', 'academic_program': 'هندسة مدنية', 'total_semesters': 8}
        )
        dept_elec, _ = Department.objects.get_or_create(
            name='قسم الهندسة الكهربائية',
            defaults={'program_type': 'بكالوريوس', 'academic_program': 'هندسة كهربائية', 'total_semesters': 8}
        )
        dept_mech, _ = Department.objects.get_or_create(
            name='قسم الهندسة الميكانيكية',
            defaults={'program_type': 'بكالوريوس', 'academic_program': 'هندسة ميكانيكية', 'total_semesters': 8}
        )
        dept_cs, _ = Department.objects.get_or_create(
            name='قسم علوم الحاسوب',
            defaults={'program_type': 'بكالوريوس', 'academic_program': 'علوم حاسوب', 'total_semesters': 8}
        )
        dept_it, _ = Department.objects.get_or_create(
            name='قسم تقنية المعلومات',
            defaults={'program_type': 'بكالوريوس', 'academic_program': 'تقنية معلومات', 'total_semesters': 8}
        )
        dept_math, _ = Department.objects.get_or_create(
            name='قسم الرياضيات',
            defaults={'program_type': 'بكالوريوس', 'academic_program': 'رياضيات', 'total_semesters': 8}
        )
        dept_phys, _ = Department.objects.get_or_create(
            name='قسم الفيزياء',
            defaults={'program_type': 'بكالوريوس', 'academic_program': 'فيزياء', 'total_semesters': 8}
        )
        dept_acc, _ = Department.objects.get_or_create(
            name='قسم المحاسبة',
            defaults={'program_type': 'بكالوريوس', 'academic_program': 'محاسبة', 'total_semesters': 8}
        )
        dept_mgmt, _ = Department.objects.get_or_create(
            name='قسم إدارة الأعمال',
            defaults={'program_type': 'بكالوريوس', 'academic_program': 'إدارة أعمال', 'total_semesters': 8}
        )

        # Assign departments to colleges
        for dept in [dept_civil, dept_elec, dept_mech]:
            CollegeDepartment.objects.get_or_create(college=col_eng, department=dept)
        for dept in [dept_cs, dept_it]:
            CollegeDepartment.objects.get_or_create(college=col_cs, department=dept)
        for dept in [dept_math, dept_phys]:
            CollegeDepartment.objects.get_or_create(college=col_sci, department=dept)
        for dept in [dept_acc, dept_mgmt]:
            CollegeDepartment.objects.get_or_create(college=col_bus, department=dept)

        all_depts = [dept_civil, dept_elec, dept_mech, dept_cs, dept_it, dept_math, dept_phys, dept_acc, dept_mgmt]

        # ── 4. Academic Years ────────────────────────
        year_names = ['السنة الأولى', 'السنة الثانية', 'السنة الثالثة', 'السنة الرابعة']
        years = []
        for i, yn in enumerate(year_names, 1):
            y, _ = AcademicYear.objects.get_or_create(year_number=i, defaults={'year_name': yn})
            years.append(y)

        # ── 5. Rooms & Halls ─────────────────────────
        rooms = []
        room_defs = [
            (col_eng, 'قاعة أ-101', 'A101', 120),
            (col_eng, 'قاعة أ-102', 'A102', 80),
            (col_eng, 'قاعة ب-201', 'B201', 60),
            (col_eng, 'قاعة ب-202', 'B202', 90),
            (col_cs,  'قاعة ت-101', 'C101', 100),
            (col_cs,  'قاعة ت-102', 'C102', 80),
            (col_cs,  'قاعة ت-201', 'C201', 60),
            (col_sci, 'قاعة د-101', 'D101', 90),
            (col_sci, 'قاعة د-102', 'D102', 60),
            (col_bus, 'قاعة هـ-101', 'E101', 80),
            (col_bus, 'قاعة هـ-102', 'E102', 60),
        ]
        for col, name, code, cap in room_defs:
            r, _ = Room.objects.get_or_create(code=code, defaults={'name': name, 'capacity': cap, 'college': col})
            CollegeRoom.objects.get_or_create(college=col, room=r, defaults={'relation_type': 'owner'})
            rooms.append(r)

        halls = []
        hall_defs = [
            (col_eng, 'معمل الحاسوب 1',   'COMP-LAB-1', 40),
            (col_eng, 'معمل الفيزياء',     'PHYS-LAB-1', 30),
            (col_eng, 'معمل الميكانيكا',   'MECH-LAB-1', 25),
            (col_cs,  'معمل البرمجة 1',    'PROG-LAB-1', 35),
            (col_cs,  'معمل البرمجة 2',    'PROG-LAB-2', 35),
            (col_cs,  'معمل الشبكات',      'NET-LAB-1',  25),
            (col_sci, 'معمل الكيمياء',     'CHEM-LAB-1', 28),
            (col_sci, 'معمل الأحياء',      'BIO-LAB-1',  28),
            (col_bus, 'معمل الحاسوب-أعمال','BUS-LAB-1',  30),
        ]
        for col, name, code, cap in hall_defs:
            h, _ = Hall.objects.get_or_create(code=code, defaults={'name': name, 'capacity': cap, 'college': col})
            CollegeHall.objects.get_or_create(college=col, hall=h, defaults={'relation_type': 'owner'})
            halls.append(h)

        # ── 6. Professors ────────────────────────────
        prof_data = [
            # (name, username, email, position, college)
            ('د. أحمد محمد علي',         'prof_ahmed',   'ahmed@sust.edu',   'دكتور',          col_eng),
            ('أ.د. سارة عبدالله',        'prof_sara',    'sara@sust.edu',    'بروفيسور',       col_eng),
            ('م. خالد إبراهيم',          'prof_khalid',  'khalid@sust.edu',  'محاضر',          col_eng),
            ('د. فاطمة النور',            'prof_fatima',  'fatima@sust.edu',  'دكتور',          col_cs),
            ('أ.د. عمر حسن',             'prof_omar',    'omar@sust.edu',    'أستاذ',          col_cs),
            ('م. رنا الطيب',              'prof_rana',    'rana@sust.edu',    'مساعد تدريس',    col_cs),
            ('د. يوسف عيسى',             'prof_yousuf',  'yousuf@sust.edu',  'دكتور',          col_sci),
            ('أ. نجلاء مصطفى',           'prof_najla',   'najla@sust.edu',   'أستاذ مشارك',   col_sci),
            ('م. بكر الأمين',             'prof_bakr',    'bakr@sust.edu',    'مساعد تدريس',    col_sci),
            ('د. هدى عثمان',             'prof_huda',    'huda@sust.edu',    'محاضر',          col_eng),
            ('د. زيد الرشيد',             'prof_zaid',    'zaid@sust.edu',    'دكتور',          col_eng),
            ('أ. سمية الحسن',             'prof_sumaya',  'sumaya@sust.edu',  'أستاذ مشارك',   col_cs),
            ('د. طارق النعيم',            'prof_tariq',   'tariq@sust.edu',   'دكتور',          col_bus),
            ('م. أمل عبدالكريم',          'prof_amal',    'amal@sust.edu',    'محاضر',          col_bus),
        ]
        prof_password = 'prof123'
        prof_hash = make_hash(prof_password)
        professors = []
        for name, uname, email, pos, col in prof_data:
            p, created = Professor.objects.get_or_create(
                username=uname,
                defaults={'name': name, 'email': email, 'position': pos, 'college': col, 'password': prof_hash}
            )
            professors.append(p)
            UnifiedUser.objects.get_or_create(
                username=uname,
                defaults={
                    'user_type': 'professor', 'user_id': p.id,
                    'full_name': name, 'email': email,
                    'college': col, 'password': prof_hash, 'is_active': True,
                }
            )
            if created:
                ProfessorCollegeRelation.objects.get_or_create(
                    professor=p, college=col, defaults={'relation_type': 'primary'}
                )

        (p_ahmed, p_sara, p_khalid, p_fatima, p_omar,
         p_rana, p_yousuf, p_najla, p_bakr, p_huda,
         p_zaid, p_sumaya, p_tariq, p_amal) = professors

        # ── 6b. System Manager (admin) ───────────────
        admin_password = 'admin123'
        admin_hash = make_hash(admin_password)
        UnifiedUser.objects.get_or_create(
            username='admin',
            defaults={
                'user_type': 'system_manager',
                'full_name': 'مدير النظام',
                'email': 'admin@sust.edu',
                'password': admin_hash,
                'is_active': True,
                'is_staff': True,
                'is_superuser': True,
            }
        )

        # ── 7. College Managers ──────────────────────
        mgr_password = 'mgr123'
        mgr_hash = make_hash(mgr_password)
        mgr_data = [
            ('mgr_eng', 'مدير_كلية', col_eng, 'م. عصام الدين',   'mgr_eng@sust.edu'),
            ('mgr_cs',  'مدير_كلية', col_cs,  'أ. منى حسين',     'mgr_cs@sust.edu'),
            ('mgr_sci', 'مدير_كلية', col_sci, 'د. ماجد سليمان',  'mgr_sci@sust.edu'),
            ('mgr_bus', 'مدير_كلية', col_bus, 'أ. لمياء الفاروق', 'mgr_bus@sust.edu'),
        ]
        for uname, role_name, col, full_name, email in mgr_data:
            role, created = Role.objects.get_or_create(
                username=uname,
                defaults={
                    'college': col, 'full_name': full_name,
                    'email': email, 'role': role_name, 'password': mgr_hash,
                }
            )
            UnifiedUser.objects.get_or_create(
                username=uname,
                defaults={
                    'user_type': 'college_manager', 'user_id': role.id,
                    'full_name': full_name, 'email': email,
                    'college': col, 'password': mgr_hash, 'is_active': True,
                }
            )

        # ── 7b. Department Heads ─────────────────────
        dh_password = 'dh123'
        dh_hash = make_hash(dh_password)
        dh_data = [
            ('dh_cs',   col_cs,  dept_cs,   'أ. هشام النور',   'dh_cs@sust.edu'),
            ('dh_it',   col_cs,  dept_it,   'أ. سلمى بشير',    'dh_it@sust.edu'),
            ('dh_elec', col_eng, dept_elec, 'م. طارق عثمان',   'dh_elec@sust.edu'),
            ('dh_civil',col_eng, dept_civil,'د. وليد النور',    'dh_civil@sust.edu'),
            ('dh_math', col_sci, dept_math, 'د. ليلى الأمين',  'dh_math@sust.edu'),
            ('dh_bus',  col_bus, dept_acc,  'أ. ريم المحمد',   'dh_bus@sust.edu'),
        ]
        for uname, col, dept, full_name, email in dh_data:
            UnifiedUser.objects.get_or_create(
                username=uname,
                defaults={
                    'user_type': 'department_head', 'user_id': 0,
                    'full_name': full_name, 'email': email,
                    'college': col, 'department': dept,
                    'password': dh_hash, 'is_active': True,
                }
            )

        # ── 8. Academic Periods ──────────────────────
        periods = {}
        for dept in all_depts:
            periods[dept.id] = {}
            for yr in years:
                periods[dept.id][yr.id] = {}
                for sem in ['1', '2']:
                    p, _ = DepartmentAcademicPeriod.objects.get_or_create(
                        department=dept, year=yr, semester_type=sem
                    )
                    periods[dept.id][yr.id][sem] = p
                    DepartmentStudentSettings.objects.get_or_create(
                        period=p, department=dept,
                        defaults={'student_count': 55 + (yr.year_number * 5), 'groups_count': 3}
                    )

        # ── 9. Specializations ───────────────────────
        spec_defs = {
            dept_cs.id: [('تخصص الذكاء الاصطناعي', years[2]), ('تخصص قواعد البيانات', years[2]), ('تخصص هندسة البرمجيات', years[2])],
            dept_it.id: [('تخصص أمن المعلومات', years[2]), ('تخصص الشبكات', years[2])],
            dept_elec.id: [('تخصص القوى الكهربائية', years[2]), ('تخصص الاتصالات', years[2])],
            dept_mech.id: [('تخصص ميكانيكا الإنتاج', years[2]), ('تخصص الطاقة الحرارية', years[2])],
            dept_acc.id: [('تخصص المحاسبة المالية', years[2]), ('تخصص مراجعة الحسابات', years[2])],
        }
        for dept_id, defs in spec_defs.items():
            for sname, yr in defs:
                p = periods[dept_id][yr.id]['1']
                Specialization.objects.get_or_create(
                    department_id=dept_id, name=sname, defaults={'period': p}
                )

        # ── 10. Courses ──────────────────────────────
        course_templates = {
            dept_civil.id: [
                ('CIVIL101', 'الرياضيات الهندسية',  3, 1, 2),
                ('CIVIL102', 'ميكانيكا الموائع',    3, 0, 3),
                ('CIVIL103', 'مقاومة المواد',        3, 1, 0),
                ('CIVIL201', 'تصميم الخرسانة',      3, 0, 2),
                ('CIVIL202', 'الجيوتقنية',           3, 1, 2),
                ('CIVIL301', 'إدارة المشاريع',       3, 1, 0),
            ],
            dept_elec.id: [
                ('ELEC101', 'دوائر كهربائية 1',     3, 1, 3),
                ('ELEC102', 'إلكترونيات أساسية',    3, 0, 3),
                ('ELEC103', 'رياضيات هندسية',       3, 1, 0),
                ('ELEC201', 'دوائر كهربائية 2',     3, 1, 3),
                ('ELEC202', 'نظرية التحكم',          3, 0, 2),
                ('ELEC301', 'الآلات الكهربائية',     3, 1, 2),
            ],
            dept_mech.id: [
                ('MECH101', 'ديناميكا الآلات',      3, 1, 2),
                ('MECH102', 'الرسم الهندسي',         2, 0, 3),
                ('MECH103', 'مقدمة في الهندسة',     3, 1, 0),
                ('MECH201', 'انتقال الحرارة',        3, 0, 2),
                ('MECH202', 'ميكانيكا المواد الصلبة',3, 1, 2),
            ],
            dept_cs.id: [
                ('CS101', 'برمجة 1',                3, 0, 3),
                ('CS102', 'هياكل البيانات',          3, 1, 2),
                ('CS103', 'الرياضيات المتقطعة',     3, 1, 0),
                ('CS201', 'خوارزميات',               3, 1, 2),
                ('CS202', 'قواعد البيانات',          3, 0, 3),
                ('CS301', 'الذكاء الاصطناعي',       3, 1, 2),
            ],
            dept_it.id: [
                ('IT101', 'مقدمة في تقنية المعلومات', 3, 0, 2),
                ('IT102', 'برمجة ويب',               3, 0, 3),
                ('IT103', 'شبكات الحاسوب',           3, 1, 2),
                ('IT201', 'أمن المعلومات',           3, 1, 2),
                ('IT202', 'إدارة النظم',             3, 0, 2),
            ],
            dept_math.id: [
                ('MATH101', 'حساب التفاضل والتكامل 1', 4, 1, 0),
                ('MATH102', 'الجبر الخطي',           3, 1, 0),
                ('MATH103', 'الإحصاء والاحتمالات',  3, 1, 0),
                ('MATH201', 'حساب التفاضل والتكامل 2', 4, 1, 0),
                ('MATH202', 'المعادلات التفاضلية',   3, 1, 0),
            ],
            dept_phys.id: [
                ('PHYS101', 'فيزياء عامة 1',         3, 1, 2),
                ('PHYS102', 'فيزياء كهرومغناطيسية',  3, 0, 2),
                ('PHYS103', 'ميكانيكا',              3, 1, 0),
                ('PHYS201', 'فيزياء عامة 2',         3, 1, 2),
                ('PHYS202', 'بصريات',                3, 0, 2),
            ],
            dept_acc.id: [
                ('ACC101', 'مبادئ المحاسبة 1',       3, 1, 0),
                ('ACC102', 'مبادئ المحاسبة 2',       3, 1, 0),
                ('ACC103', 'الرياضيات المالية',      3, 1, 0),
                ('ACC201', 'محاسبة التكاليف',         3, 0, 2),
                ('ACC202', 'تحليل القوائم المالية',  3, 1, 0),
            ],
            dept_mgmt.id: [
                ('MGT101', 'مبادئ الإدارة',          3, 1, 0),
                ('MGT102', 'الاقتصاد الجزئي',        3, 1, 0),
                ('MGT103', 'إدارة الموارد البشرية',  3, 0, 0),
                ('MGT201', 'إدارة التسويق',           3, 1, 0),
                ('MGT202', 'القيادة والاستراتيجية',  3, 1, 0),
            ],
        }

        courses = {}
        for dept_id, cdefs in course_templates.items():
            courses[dept_id] = {}
            yr1_s1 = periods[dept_id][years[0].id]['1']
            yr2_s1 = periods[dept_id][years[1].id]['1']
            yr3_s1 = periods[dept_id][years[2].id]['1']
            for i, (code, name, lh, eh, labh) in enumerate(cdefs):
                if i < 3:
                    period = yr1_s1
                elif i < 5:
                    period = yr2_s1
                else:
                    period = yr3_s1
                c, _ = Course.objects.get_or_create(
                    course_code=code,
                    defaults={
                        'period': period, 'course_name': name,
                        'lecture_hours': lh, 'exercise_hours': eh, 'lab_hours': labh,
                        'total_lectures': lh * 14,
                    }
                )
                courses[dept_id][code] = c

        # ── 11. Students ─────────────────────────────
        std_password = 'std123'
        std_hash = make_hash(std_password)
        student_defs = [
            # (name, username, email, dept, year_idx, sem)
            ('علي عمر محمد',       'std_ali',      'ali@student.sust.edu',      dept_cs,    0, '1'),
            ('مريم خالد',          'std_maryam',   'maryam@student.sust.edu',   dept_cs,    0, '1'),
            ('إبراهيم سعد',        'std_ibrahim',  'ibrahim@student.sust.edu',  dept_it,    0, '1'),
            ('سلمى حسن',           'std_salma',    'salma@student.sust.edu',    dept_it,    1, '1'),
            ('أسامة بشير',         'std_osama',    'osama@student.sust.edu',    dept_civil, 0, '1'),
            ('منال أحمد',          'std_manal',    'manal@student.sust.edu',    dept_elec,  0, '1'),
            ('كريم عبدالرحمن',     'std_karim',    'karim@student.sust.edu',    dept_math,  1, '2'),
            ('نورا الفاضل',        'std_nora',     'nora@student.sust.edu',     dept_phys,  0, '1'),
            ('يحيى الطيب',         'std_yahya',    'yahya@student.sust.edu',    dept_cs,    1, '1'),
            ('أميرة صالح',         'std_amira',    'amira@student.sust.edu',    dept_cs,    2, '1'),
            ('حسام الدين',         'std_husam',    'husam@student.sust.edu',    dept_it,    0, '1'),
            ('رانيا إدريس',        'std_rania',    'rania@student.sust.edu',    dept_elec,  1, '1'),
            ('ماهر عبدالله',       'std_maher',    'maher@student.sust.edu',    dept_mech,  0, '1'),
            ('لمى الزبير',          'std_lama',     'lama@student.sust.edu',     dept_acc,   0, '1'),
            ('صهيب الحاج',         'std_sohayb',   'sohayb@student.sust.edu',   dept_mgmt,  0, '1'),
        ]
        students = []
        for sname, uname, email, dept, yr_idx, sem in student_defs:
            period = periods[dept.id][years[yr_idx].id][sem]
            std, created = Student.objects.get_or_create(
                username=uname,
                defaults={'name': sname, 'email': email, 'department': dept, 'period': period, 'password': std_hash}
            )
            students.append(std)
            UnifiedUser.objects.get_or_create(
                username=uname,
                defaults={
                    'user_type': 'student', 'user_id': std.id,
                    'full_name': sname, 'email': email,
                    'department': dept, 'password': std_hash, 'is_active': True,
                }
            )

        # ── 12. Lecture Schedules ────────────────────
        DAYS = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday']

        def make_time(h, m=0):
            return time(h, m)

        r_eng = [r for r in rooms if r.college == col_eng]
        r_cs  = [r for r in rooms if r.college == col_cs]
        r_sci = [r for r in rooms if r.college == col_sci]
        r_bus = [r for r in rooms if r.college == col_bus]

        lecture_defs = [
            # CS dept, Year1 Sem1
            (dept_cs, periods[dept_cs.id][years[0].id]['1'], 'CS101', p_fatima, r_cs[0], 'Saturday',  8,  0, 10, 0, 'lecture'),
            (dept_cs, periods[dept_cs.id][years[0].id]['1'], 'CS101', p_fatima, r_cs[0], 'Tuesday',   8,  0, 10, 0, 'lecture'),
            (dept_cs, periods[dept_cs.id][years[0].id]['1'], 'CS102', p_omar,   r_cs[1], 'Sunday',   10,  0, 12, 0, 'lecture'),
            (dept_cs, periods[dept_cs.id][years[0].id]['1'], 'CS102', p_omar,   r_cs[1], 'Wednesday',10,  0, 12, 0, 'lecture'),
            (dept_cs, periods[dept_cs.id][years[0].id]['1'], 'CS103', p_rana,   r_cs[0], 'Monday',   12,  0, 14, 0, 'lecture'),
            (dept_cs, periods[dept_cs.id][years[0].id]['1'], 'CS103', p_rana,   r_cs[0], 'Thursday', 12,  0, 14, 0, 'lecture'),
            # CS dept, Year2 Sem1
            (dept_cs, periods[dept_cs.id][years[1].id]['1'], 'CS201', p_fatima, r_cs[0], 'Saturday', 10,  0, 12, 0, 'lecture'),
            (dept_cs, periods[dept_cs.id][years[1].id]['1'], 'CS201', p_fatima, r_cs[0], 'Wednesday',10,  0, 12, 0, 'lecture'),
            (dept_cs, periods[dept_cs.id][years[1].id]['1'], 'CS202', p_omar,   r_cs[1], 'Sunday',    8,  0, 10, 0, 'lecture'),
            (dept_cs, periods[dept_cs.id][years[1].id]['1'], 'CS202', p_omar,   r_cs[1], 'Thursday',  8,  0, 10, 0, 'lecture'),
            # CS dept, Year3 Sem1
            (dept_cs, periods[dept_cs.id][years[2].id]['1'], 'CS301', p_sumaya, r_cs[2], 'Sunday',    14,  0, 16, 0, 'lecture'),
            (dept_cs, periods[dept_cs.id][years[2].id]['1'], 'CS301', p_sumaya, r_cs[2], 'Wednesday', 14,  0, 16, 0, 'lecture'),
            # IT dept, Year1 Sem1
            (dept_it, periods[dept_it.id][years[0].id]['1'], 'IT101', p_rana,   r_cs[0], 'Saturday',  14,  0, 16, 0, 'lecture'),
            (dept_it, periods[dept_it.id][years[0].id]['1'], 'IT101', p_rana,   r_cs[0], 'Tuesday',   14,  0, 16, 0, 'lecture'),
            (dept_it, periods[dept_it.id][years[0].id]['1'], 'IT102', p_fatima, r_cs[1], 'Sunday',    12,  0, 14, 0, 'lecture'),
            (dept_it, periods[dept_it.id][years[0].id]['1'], 'IT103', p_omar,   r_cs[0], 'Monday',     8,  0, 10, 0, 'lecture'),
            # IT dept, Year2 Sem1
            (dept_it, periods[dept_it.id][years[1].id]['1'], 'IT201', p_sumaya, r_cs[1], 'Saturday',   8,  0, 10, 0, 'lecture'),
            (dept_it, periods[dept_it.id][years[1].id]['1'], 'IT202', p_rana,   r_cs[0], 'Monday',    14,  0, 16, 0, 'lecture'),
            # Civil dept, Year1 Sem1
            (dept_civil, periods[dept_civil.id][years[0].id]['1'], 'CIVIL101', p_ahmed,  r_eng[0], 'Saturday',   8,  0, 10, 0, 'lecture'),
            (dept_civil, periods[dept_civil.id][years[0].id]['1'], 'CIVIL101', p_ahmed,  r_eng[0], 'Monday',     8,  0, 10, 0, 'lecture'),
            (dept_civil, periods[dept_civil.id][years[0].id]['1'], 'CIVIL102', p_sara,   r_eng[1], 'Sunday',    10,  0, 12, 0, 'lecture'),
            (dept_civil, periods[dept_civil.id][years[0].id]['1'], 'CIVIL102', p_sara,   r_eng[1], 'Wednesday', 10,  0, 12, 0, 'lecture'),
            (dept_civil, periods[dept_civil.id][years[0].id]['1'], 'CIVIL103', p_khalid, r_eng[2], 'Tuesday',   12,  0, 14, 0, 'lecture'),
            (dept_civil, periods[dept_civil.id][years[0].id]['1'], 'CIVIL103', p_khalid, r_eng[2], 'Thursday',  12,  0, 14, 0, 'lecture'),
            # Civil dept, Year2 Sem1
            (dept_civil, periods[dept_civil.id][years[1].id]['1'], 'CIVIL201', p_zaid,   r_eng[3], 'Saturday',  10,  0, 12, 0, 'lecture'),
            (dept_civil, periods[dept_civil.id][years[1].id]['1'], 'CIVIL202', p_ahmed,  r_eng[0], 'Sunday',    14,  0, 16, 0, 'lecture'),
            # Elec dept, Year1 Sem1
            (dept_elec, periods[dept_elec.id][years[0].id]['1'], 'ELEC101', p_huda,   r_eng[0], 'Saturday',  10,  0, 12, 0, 'lecture'),
            (dept_elec, periods[dept_elec.id][years[0].id]['1'], 'ELEC101', p_huda,   r_eng[0], 'Wednesday', 10,  0, 12, 0, 'lecture'),
            (dept_elec, periods[dept_elec.id][years[0].id]['1'], 'ELEC102', p_ahmed,  r_eng[1], 'Sunday',     8,  0, 10, 0, 'lecture'),
            (dept_elec, periods[dept_elec.id][years[0].id]['1'], 'ELEC102', p_ahmed,  r_eng[1], 'Tuesday',    8,  0, 10, 0, 'lecture'),
            (dept_elec, periods[dept_elec.id][years[0].id]['1'], 'ELEC103', p_sara,   r_eng[2], 'Monday',    14,  0, 16, 0, 'lecture'),
            # Mech dept, Year1 Sem1
            (dept_mech, periods[dept_mech.id][years[0].id]['1'], 'MECH101', p_zaid,   r_eng[3], 'Saturday',  12,  0, 14, 0, 'lecture'),
            (dept_mech, periods[dept_mech.id][years[0].id]['1'], 'MECH102', p_khalid, r_eng[2], 'Sunday',    14,  0, 16, 0, 'lecture'),
            (dept_mech, periods[dept_mech.id][years[0].id]['1'], 'MECH103', p_sara,   r_eng[1], 'Monday',    10,  0, 12, 0, 'lecture'),
            # Math dept, Year1 Sem1
            (dept_math, periods[dept_math.id][years[0].id]['1'], 'MATH101', p_yousuf, r_sci[0], 'Saturday',   8,  0, 10, 0, 'lecture'),
            (dept_math, periods[dept_math.id][years[0].id]['1'], 'MATH101', p_yousuf, r_sci[0], 'Tuesday',    8,  0, 10, 0, 'lecture'),
            (dept_math, periods[dept_math.id][years[0].id]['1'], 'MATH102', p_najla,  r_sci[1], 'Sunday',    10,  0, 12, 0, 'lecture'),
            (dept_math, periods[dept_math.id][years[0].id]['1'], 'MATH102', p_najla,  r_sci[1], 'Thursday',  10,  0, 12, 0, 'lecture'),
            (dept_math, periods[dept_math.id][years[0].id]['1'], 'MATH103', p_bakr,   r_sci[0], 'Monday',    12,  0, 14, 0, 'lecture'),
            # Physics dept, Year1 Sem1
            (dept_phys, periods[dept_phys.id][years[0].id]['1'], 'PHYS101', p_najla,  r_sci[0], 'Saturday',  12,  0, 14, 0, 'lecture'),
            (dept_phys, periods[dept_phys.id][years[0].id]['1'], 'PHYS101', p_najla,  r_sci[0], 'Wednesday', 12,  0, 14, 0, 'lecture'),
            (dept_phys, periods[dept_phys.id][years[0].id]['1'], 'PHYS102', p_yousuf, r_sci[1], 'Sunday',     8,  0, 10, 0, 'lecture'),
            (dept_phys, periods[dept_phys.id][years[0].id]['1'], 'PHYS103', p_bakr,   r_sci[0], 'Monday',    10,  0, 12, 0, 'lecture'),
            # Business dept, Year1 Sem1
            (dept_acc,  periods[dept_acc.id][years[0].id]['1'],  'ACC101',  p_tariq,  r_bus[0], 'Saturday',   8,  0, 10, 0, 'lecture'),
            (dept_acc,  periods[dept_acc.id][years[0].id]['1'],  'ACC101',  p_tariq,  r_bus[0], 'Tuesday',    8,  0, 10, 0, 'lecture'),
            (dept_acc,  periods[dept_acc.id][years[0].id]['1'],  'ACC102',  p_amal,   r_bus[1], 'Sunday',    10,  0, 12, 0, 'lecture'),
            (dept_acc,  periods[dept_acc.id][years[0].id]['1'],  'ACC103',  p_tariq,  r_bus[0], 'Monday',    12,  0, 14, 0, 'lecture'),
            (dept_mgmt, periods[dept_mgmt.id][years[0].id]['1'], 'MGT101',  p_amal,   r_bus[1], 'Saturday',  10,  0, 12, 0, 'lecture'),
            (dept_mgmt, periods[dept_mgmt.id][years[0].id]['1'], 'MGT102',  p_tariq,  r_bus[0], 'Sunday',    14,  0, 16, 0, 'lecture'),
            (dept_mgmt, periods[dept_mgmt.id][years[0].id]['1'], 'MGT103',  p_amal,   r_bus[1], 'Monday',     8,  0, 10, 0, 'lecture'),
        ]

        lecture_objs = []
        for dept, period, code, prof, room, day, sh, sm, eh, em, ltype in lecture_defs:
            dept_id = dept.id
            c = courses[dept_id].get(code)
            if not c:
                continue
            lec, _ = LectureSchedule.objects.get_or_create(
                department=dept, period=period, course=c,
                professor=prof, room=room, day_of_week=day,
                start_time=make_time(sh, sm), end_time=make_time(eh, em),
                defaults={'lecture_type': ltype}
            )
            lecture_objs.append(lec)

        # ── 13. Lab Schedules ────────────────────────
        h_eng = [h for h in halls if h.college == col_eng]
        h_cs  = [h for h in halls if h.college == col_cs]
        h_sci = [h for h in halls if h.college == col_sci]
        h_bus = [h for h in halls if h.college == col_bus]

        lab_defs = [
            (dept_cs,    periods[dept_cs.id][years[0].id]['1'],    'CS101',  p_fatima, p_rana,    h_cs[0],  'Monday',     10, 0, 12, 0, 1),
            (dept_cs,    periods[dept_cs.id][years[0].id]['1'],    'CS101',  p_fatima, p_rana,    h_cs[0],  'Thursday',   10, 0, 12, 0, 2),
            (dept_cs,    periods[dept_cs.id][years[0].id]['1'],    'CS101',  p_sumaya, p_rana,    h_cs[1],  'Saturday',   14, 0, 16, 0, 3),
            (dept_cs,    periods[dept_cs.id][years[0].id]['1'],    'CS102',  p_omar,   p_rana,    h_cs[1],  'Tuesday',    14, 0, 16, 0, 1),
            (dept_cs,    periods[dept_cs.id][years[1].id]['1'],    'CS202',  p_omar,   None,      h_cs[0],  'Monday',      8, 0, 10, 0, 1),
            (dept_cs,    periods[dept_cs.id][years[1].id]['1'],    'CS202',  p_sumaya, None,      h_cs[1],  'Wednesday',   8, 0, 10, 0, 2),
            (dept_it,    periods[dept_it.id][years[0].id]['1'],    'IT101',  p_rana,   None,      h_cs[1],  'Saturday',   12, 0, 14, 0, 1),
            (dept_it,    periods[dept_it.id][years[0].id]['1'],    'IT103',  p_omar,   p_fatima,  h_cs[0],  'Wednesday',  14, 0, 16, 0, 1),
            (dept_civil, periods[dept_civil.id][years[0].id]['1'], 'CIVIL102',p_sara,  p_khalid,  h_eng[0], 'Saturday',   12, 0, 14, 0, 1),
            (dept_civil, periods[dept_civil.id][years[0].id]['1'], 'CIVIL102',p_sara,  p_khalid,  h_eng[0], 'Tuesday',    12, 0, 14, 0, 2),
            (dept_elec,  periods[dept_elec.id][years[0].id]['1'],  'ELEC101', p_huda,  p_ahmed,   h_eng[1], 'Sunday',     14, 0, 16, 0, 1),
            (dept_elec,  periods[dept_elec.id][years[0].id]['1'],  'ELEC102', p_ahmed, None,      h_eng[0], 'Thursday',    8, 0, 10, 0, 1),
            (dept_mech,  periods[dept_mech.id][years[0].id]['1'],  'MECH102', p_khalid, p_zaid,   h_eng[2], 'Saturday',   14, 0, 16, 0, 1),
            (dept_math,  periods[dept_math.id][years[0].id]['1'],  'MATH101', p_yousuf, p_bakr,   h_sci[0], 'Saturday',   14, 0, 16, 0, 1),
            (dept_phys,  periods[dept_phys.id][years[0].id]['1'],  'PHYS101', p_najla,  p_bakr,   h_sci[1], 'Monday',     14, 0, 16, 0, 1),
            (dept_phys,  periods[dept_phys.id][years[0].id]['1'],  'PHYS102', p_yousuf, None,     h_sci[0], 'Wednesday',   8, 0, 10, 0, 1),
            (dept_acc,   periods[dept_acc.id][years[0].id]['1'],   'ACC101',  p_tariq,  p_amal,   h_bus[0], 'Thursday',   12, 0, 14, 0, 1),
        ]

        for dept, period, code, prof, asst, hall, day, sh, sm, eh, em, grp in lab_defs:
            c = courses[dept.id].get(code)
            if not c:
                continue
            LabSchedule.objects.get_or_create(
                department=dept, period=period, course=c,
                professor=prof, hall=hall, day_of_week=day,
                start_time=make_time(sh, sm), end_time=make_time(eh, em),
                group_number=grp,
                defaults={'assistant': asst}
            )

        # ── 14. AlternativeTime Requests (diverse scenarios) ──
        lec_sample = lecture_objs[:8] if len(lecture_objs) >= 8 else lecture_objs
        request_defs = [
            (p_fatima, lec_sample[0] if lec_sample else None, 'pending',
             'سفر خارجي للمشاركة في مؤتمر علمي دولي', 'Monday', 14, 0, 16, 0),
            (p_omar,   lec_sample[2] if len(lec_sample) > 2 else None, 'approved',
             'ظروف صحية طارئة تستدعي مراجعة طبية', 'Wednesday', 8, 0, 10, 0),
            (p_ahmed,  lec_sample[4] if len(lec_sample) > 4 else None, 'rejected',
             'ارتباطات خارجية مع جهة حكومية', 'Tuesday', 12, 0, 14, 0),
            (p_sara,   None, 'pending',
             'اجتماع مجلس القسم الطارئ', 'Thursday', 10, 0, 12, 0),
            (p_khalid, lec_sample[1] if len(lec_sample) > 1 else None, 'approved',
             'انقطاع كهربائي في مبنى القسم', 'Sunday', 8, 0, 10, 0),
            (p_huda,   None, 'pending',
             'حضور ورشة تدريبية لتطوير المناهج', 'Saturday', 14, 0, 16, 0),
            (p_yousuf, lec_sample[5] if len(lec_sample) > 5 else None, 'rejected',
             'لا يوجد بديل متاح في نفس التوقيت', 'Monday', 10, 0, 12, 0),
            (p_najla,  lec_sample[6] if len(lec_sample) > 6 else None, 'approved',
             'اجتماع لجنة الاعتماد الأكاديمي', 'Saturday', 10, 0, 12, 0),
            (p_rana,   lec_sample[3] if len(lec_sample) > 3 else None, 'pending',
             'مناقشة رسالة ماجستير', 'Wednesday', 12, 0, 14, 0),
            (p_tariq,  None, 'approved',
             'زيارة ميدانية لشركة شريكة', 'Sunday', 12, 0, 14, 0),
        ]
        for prof, sched, status, notes, day, sh, sm, eh, em in request_defs:
            AlternativeTime.objects.get_or_create(
                professor=prof,
                day=day,
                time_start=make_time(sh, sm),
                defaults={
                    'schedule': sched,
                    'course_name': sched.course.course_name if sched else 'مادة عامة',
                    'original_day': sched.day_of_week if sched else day,
                    'original_time_start': sched.start_time if sched else make_time(sh, sm),
                    'original_time_end': sched.end_time if sched else make_time(eh, em),
                    'time_start': make_time(sh, sm),
                    'time_end': make_time(eh, em),
                    'notes': notes,
                    'status': status,
                    'admin_notes': 'تمت الموافقة على الطلب' if status == 'approved' else (
                        'تم الرفض لعدم توفر قاعة أو بديل مناسب' if status == 'rejected' else ''),
                }
            )

        # ── 15. Taught Lectures ──────────────────────
        today = date.today()
        for i, lec in enumerate(lecture_objs[:15]):
            for delta in [7, 14, 21, 28]:
                TaughtLecture.objects.get_or_create(
                    schedule=lec,
                    taught_date=today - timedelta(days=delta),
                    defaults={'professor': lec.professor, 'notification_sent': True}
                )

        # ── 16. Notifications (rich & diverse) ───────
        admin_user = UnifiedUser.objects.filter(user_type='system_manager').first()
        prof_users = list(UnifiedUser.objects.filter(user_type='professor'))
        std_users  = list(UnifiedUser.objects.filter(user_type='student'))
        mgr_users  = list(UnifiedUser.objects.filter(user_type='college_manager'))

        notif_defs = []
        if admin_user:
            notif_defs += [
                (admin_user, 'طلب تغيير موعد جديد',         'قدّم الدكتور أحمد محمد طلب تغيير موعد المحاضرة للنظر فيه', False),
                (admin_user, 'تقرير أسبوعي',                 'تم إنشاء التقرير الأسبوعي للجداول الدراسية بنجاح', True),
                (admin_user, 'تعارض في الجدول',              'تم رصد تعارض في توقيت قاعة أ-101 يوم السبت الساعة 10:00', False),
                (admin_user, 'إضافة أستاذ جديد',             'تمت إضافة الأستاذ الدكتور زيد الرشيد إلى قسم الهندسة المدنية', True),
                (admin_user, 'تحديث إعدادات النظام',         'تم تحديث إعدادات النظام وتفعيل ميزة التصدير التلقائي', False),
                (admin_user, 'انتهاء الموعد النهائي قريباً', 'تبقى أسبوعان على انتهاء الموعد النهائي لتسليم الجداول', False),
            ]

        for i, pu in enumerate(prof_users[:8]):
            msgs = [
                ('تحديث في الجدول الدراسي',       'تم تعديل موعد إحدى محاضراتك، يرجى مراجعة جدولك', False),
                ('موافقة على طلب تغيير الموعد',   'تمت الموافقة على طلبك لتغيير موعد المحاضرة', False),
                ('رفض طلب تغيير الموعد',           'تم رفض طلب تغيير الموعد، يرجى التواصل مع مدير الكلية', True),
                ('تذكير بتسليم التقارير',          'يرجى تسليم تقرير المحاضرات المُدرَّسة لهذا الأسبوع', False),
                ('إشعار بتغيير القاعة',             'تم تغيير قاعة محاضرتك من أ-101 إلى ب-201 ليوم الأحد', False),
                ('دعوة لاجتماع القسم',              'لديك اجتماع قسم يوم الثلاثاء القادم الساعة 11:00', True),
                ('إشعار بجدول جديد',               'تم نشر جدول الفصل الدراسي الجديد، يرجى المراجعة', False),
                ('طلب تأكيد المحاضرات',            'يرجى تأكيد حضور محاضراتك للأسبوع القادم', False),
            ]
            subj, msg, is_read = msgs[i % len(msgs)]
            notif_defs.append((pu, subj, msg, is_read))

        for i, su in enumerate(std_users[:10]):
            msgs = [
                ('تحديث جدولك الدراسي',           'تم تحديث جدولك الدراسي لهذا الفصل، يرجى مراجعة التغييرات', False),
                ('إلغاء محاضرة',                   'تم إلغاء محاضرة مادة قواعد البيانات يوم الأحد', False),
                ('تغيير موعد المحاضرة',            'تم تغيير موعد محاضرة البرمجة من 8:00 إلى 10:00', True),
                ('تغيير قاعة الدراسة',             'سيتم عقد محاضرة هياكل البيانات في قاعة ت-201 بدلاً من ت-101', False),
                ('إشعار بالاختبار',                'اختبار منتصف الفصل لمادة الرياضيات المتقطعة الأسبوع القادم', False),
                ('تعديل في الجدول العام',          'تم إجراء تعديلات على جدول الفصل الثاني، راجع لوحة الإعلانات', True),
                ('إشعار بالمعمل',                  'موعد معمل البرمجة تغير إلى يوم الخميس الساعة 10:00', False),
                ('تذكير بتسليم المشروع',           'تذكير: الموعد النهائي لتسليم مشروع قواعد البيانات هو الجمعة', False),
                ('إلغاء معمل الشبكات',             'تم إلغاء معمل الشبكات هذا الأسبوع بسبب صيانة الأجهزة', False),
                ('استئناف المحاضرات',              'ستُستأنف محاضرات مادة الخوارزميات اعتباراً من الأحد القادم', True),
            ]
            subj, msg, is_read = msgs[i % len(msgs)]
            notif_defs.append((su, subj, msg, is_read))

        for i, mu in enumerate(mgr_users[:4]):
            msgs = [
                ('طلب تغيير موعد يحتاج مراجعة',   'قدّم أستاذ طلباً لتغيير موعد محاضرته، يرجى المراجعة والبت فيه', False),
                ('تقرير أسبوعي للكلية',             'تم إعداد التقرير الأسبوعي لجداول الكلية وهو جاهز للمراجعة', False),
                ('إشعار بانتهاء الموعد النهائي',   'اقترب الموعد النهائي لتقديم جداول الفصل الدراسي الجديد', True),
                ('رسالة من مدير النظام',            'يرجى مراجعة الإعدادات الجديدة للنظام وتأكيد تطبيقها على الكلية', False),
            ]
            subj, msg, is_read = msgs[i % len(msgs)]
            notif_defs.append((mu, subj, msg, is_read))

        for recipient, subj, msg, is_read in notif_defs:
            Notification.objects.get_or_create(
                recipient=recipient, subject=subj,
                defaults={'message': msg, 'status': 'sent', 'is_read': is_read}
            )

        # ── 17. Schedule Deadline ────────────────────
        ScheduleDeadline.objects.get_or_create(
            deadline_date=today + timedelta(days=21)
        )

        # ── 18. Schedule Change Log ──────────────────
        if admin_user and lecture_objs:
            log_defs = [
                (lecture_objs[0], 'add',    {'day': 'Saturday',  'start': '08:00', 'room': 'C101'}, None,
                 'إضافة محاضرة جديدة في بداية الفصل الدراسي'),
                (lecture_objs[1], 'edit',   {'day': 'Tuesday',   'start': '08:00', 'room': 'C101'},
                 {'day': 'Monday', 'start': '10:00', 'room': 'C102'},
                 'تعديل موعد المحاضرة بسبب تعارض مع قسم آخر'),
                (lecture_objs[2], 'add',    {'day': 'Sunday',    'start': '10:00', 'room': 'C102'}, None,
                 'إضافة محاضرة إضافية لتعويض أيام الإجازة'),
                (lecture_objs[4], 'edit',   {'day': 'Saturday',  'start': '08:00', 'room': 'A101'},
                 {'day': 'Saturday', 'start': '10:00', 'room': 'A102'},
                 'تغيير القاعة لاستيعاب عدد الطلاب الكبير'),
                (lecture_objs[5], 'delete', None,
                 {'day': 'Wednesday', 'start': '10:00', 'room': 'A101'},
                 'حذف المحاضرة بسبب إلغاء المادة في هذا الفصل'),
                (lecture_objs[6], 'add',    {'day': 'Monday',    'start': '14:00', 'room': 'C101'}, None,
                 'إضافة محاضرة إضافية بناءً على طلب رئيس القسم'),
            ]
            for entry in log_defs:
                lec, action = entry[0], entry[1]
                new_data, old_data, reason = entry[2], entry[3], entry[4]
                ScheduleChangeLog.objects.get_or_create(
                    schedule_type='lecture', schedule_id=lec.id, action=action,
                    defaults={
                        'changed_by': admin_user,
                        'old_data': old_data,
                        'new_data': new_data,
                        'department_name': lec.department.name,
                        'course_name': lec.course.course_name,
                        'change_reason': reason,
                    }
                )

    def _print_credentials(self):
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('═' * 65))
        self.stdout.write(self.style.SUCCESS('  بيانات الدخول للاختبار'))
        self.stdout.write(self.style.SUCCESS('═' * 65))
        rows = [
            ('الدور',                        'اسم المستخدم',  'كلمة المرور'),
            ('─' * 30,                       '─' * 16,         '─' * 10),
            ('مدير النظام',                  'admin',          'admin123'),
            ('مدير كلية الهندسة',            'mgr_eng',        'mgr123'),
            ('مدير كلية الحاسوب',            'mgr_cs',         'mgr123'),
            ('مدير كلية العلوم',             'mgr_sci',        'mgr123'),
            ('مدير كلية إدارة الأعمال',     'mgr_bus',        'mgr123'),
            ('رئيس قسم الحاسوب',            'dh_cs',          'dh123'),
            ('رئيس قسم تقنية المعلومات',    'dh_it',          'dh123'),
            ('رئيس قسم الهندسة الكهربائية', 'dh_elec',        'dh123'),
            ('رئيس قسم الهندسة المدنية',    'dh_civil',       'dh123'),
            ('رئيس قسم الرياضيات',          'dh_math',        'dh123'),
            ('رئيس قسم المحاسبة',           'dh_bus',         'dh123'),
            ('أستاذ - د. فاطمة',            'prof_fatima',    'prof123'),
            ('أستاذ - د. أحمد',             'prof_ahmed',     'prof123'),
            ('أستاذ - أ.د. عمر',            'prof_omar',      'prof123'),
            ('أستاذ - أ.د. سارة',           'prof_sara',      'prof123'),
            ('أستاذ - م. خالد',             'prof_khalid',    'prof123'),
            ('أستاذ - د. يوسف',             'prof_yousuf',    'prof123'),
            ('أستاذ - د. طارق (أعمال)',      'prof_tariq',     'prof123'),
            ('طالب - علي (حاسوب س1)',        'std_ali',        'std123'),
            ('طالب - مريم (حاسوب س1)',       'std_maryam',     'std123'),
            ('طالب - أسامة (مدني س1)',       'std_osama',      'std123'),
            ('طالب - يحيى (حاسوب س2)',       'std_yahya',      'std123'),
            ('طالب - أميرة (حاسوب س3)',     'std_amira',      'std123'),
            ('طالب - ماهر (ميكانيكا)',       'std_maher',      'std123'),
            ('طالب - لمى (محاسبة)',          'std_lama',       'std123'),
        ]
        for role, uname, pw in rows:
            self.stdout.write(f'  {role:<35} {uname:<18} {pw}')
        self.stdout.write(self.style.SUCCESS('═' * 65))
