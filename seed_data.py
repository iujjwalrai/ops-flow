import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from users.models import User
from organizations.models import Organization, OrganizationMember
from projects.models import Project
from tasks.models import Task


def run():
    print("🌱 Seeding OpsFlow...")

    # -------------------------
    # Users
    # -------------------------

    users = []

    user_data = [
        ("ujjwal", "ujjwal@example.com", "Ujjwal", "Rai"),
        ("rahul", "rahul@example.com", "Rahul", "Sharma"),
        ("aman", "aman@example.com", "Aman", "Singh"),
        ("priya", "priya@example.com", "Priya", "Verma"),
    ]

    for username, email, first_name, last_name in user_data:
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
            },
        )

        if created:
            user.set_password("password123")
            user.save()

        users.append(user)

    ujjwal, rahul, aman, priya = users

    # -------------------------
    # Organizations
    # -------------------------

    org1, _ = Organization.objects.get_or_create(
        name="OpsFlow Engineering"
    )

    org2, _ = Organization.objects.get_or_create(
        name="Acme Technologies"
    )

    # -------------------------
    # Organization Members
    # -------------------------

    memberships = [
        (org1, ujjwal, OrganizationMember.Role.OWNER),
        (org1, rahul, OrganizationMember.Role.ADMIN),
        (org1, aman, OrganizationMember.Role.MEMBER),

        (org2, priya, OrganizationMember.Role.OWNER),
        (org2, aman, OrganizationMember.Role.MEMBER),
    ]

    for organization, user, role in memberships:
        OrganizationMember.objects.get_or_create(
            organization=organization,
            user=user,
            defaults={"role": role},
        )

    # -------------------------
    # Projects
    # -------------------------

    backend, _ = Project.objects.get_or_create(
        organization=org1,
        name="OpsFlow Backend",
        defaults={
            "description": "Main Django backend",
            "created_by": ujjwal,
        },
    )

    mobile, _ = Project.objects.get_or_create(
        organization=org1,
        name="Mobile Application",
        defaults={
            "description": "OpsFlow mobile application",
            "created_by": rahul,
        },
    )

    website, _ = Project.objects.get_or_create(
        organization=org2,
        name="Company Website",
        defaults={
            "description": "Corporate website",
            "created_by": priya,
        },
    )

    # -------------------------
    # Tasks
    # -------------------------

    tasks = [
        (
            backend,
            "Implement JWT authentication",
            "Build login and token authentication",
            ujjwal,
            Task.Status.IN_PROGRESS,
            Task.Priority.HIGH,
        ),
        (
            backend,
            "Build project APIs",
            "Create CRUD APIs for projects",
            rahul,
            Task.Status.DONE,
            Task.Priority.HIGH,
        ),
        (
            backend,
            "Add Redis caching",
            "Cache frequently accessed project data",
            aman,
            Task.Status.TODO,
            Task.Priority.MEDIUM,
        ),
        (
            mobile,
            "Create login screen",
            "Implement mobile login UI",
            aman,
            Task.Status.IN_PROGRESS,
            Task.Priority.MEDIUM,
        ),
        (
            website,
            "Build landing page",
            "Create company landing page",
            priya,
            Task.Status.TODO,
            Task.Priority.LOW,
        ),
    ]

    for (
        project,
        title,
        description,
        assigned_to,
        status,
        priority,
    ) in tasks:

        Task.objects.get_or_create(
            project=project,
            title=title,
            defaults={
                "description": description,
                "assigned_to": assigned_to,
                "status": status,
                "priority": priority,
            },
        )

    print("✅ Seed completed!")
    print()
    print("Users:")
    print("  ujjwal / password123")
    print("  rahul  / password123")
    print("  aman   / password123")
    print("  priya  / password123")
    print()
    print(f"Organizations: {Organization.objects.count()}")
    print(f"Projects:      {Project.objects.count()}")
    print(f"Tasks:         {Task.objects.count()}")


if __name__ == "__main__":
    run()