from django.core.management.base import BaseCommand
from django.utils.text import slugify
from guides.models import Guide, Paragraph
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "Populate 4 useful fixed guides with paragraphs"

    def handle(self, *args, **options):
        users = list(User.objects.all())
        if not users:
            self.stdout.write(self.style.ERROR("❌ No users found. Create a user first."))
            return

        user = users[0]  # use first user

        guides_data = [
          {
    "title": "What to do when your dog is lost",
    "description": "Follow these essential steps immediately to increase the chances of safely finding your lost dog.",
    "paragraphs": [
        {
            "step_title": "Stay Calm and Act Quickly",
            "content": "Try to stay calm and focus on taking immediate action. The faster you start searching and notifying others, the better the chances of finding your dog."
        },
        {
            "step_title": "Search Your Immediate Area",
            "content": "Begin by thoroughly checking your home, yard, and the surrounding neighborhood. Dogs often don’t wander far initially and might be hiding nearby."
        },
        {
            "step_title": "Notify Neighbors and Local Community",
            "content": "Inform your neighbors and ask them to keep an eye out. Share your dog's description and contact information."
        },
        {
            "step_title": "Use Social Media and Online Platforms",
            "content": "Post clear photos and detailed descriptions on social media sites, lost pet groups, and community forums to reach a wider audience quickly."
        },
        {
            "step_title": "Create and Distribute Flyers",
            "content": "Make flyers with your dog's photo, description, and your contact details. Post them around your neighborhood, parks, vet clinics, and local stores."
        },
        {
            "step_title": "Contact Animal Shelters and Vets",
            "content": "Call nearby animal shelters, rescue organizations, and veterinary offices. Visit shelters in person regularly as phone reports may be incomplete."
        },
        {
            "step_title": "Use Familiar Scents to Attract Your Dog",
            "content": "Leave your dog's bedding, toys, or your worn clothing outside your home to help guide them back through scent."
        },
        {
            "step_title": "Check Lost Pet Websites and Apps",
            "content": "Register your lost dog on popular lost pet databases and apps. Also, check for found dog reports that may match your pet."
        },
        {
            "step_title": "Keep Your Phone Nearby and Stay Available",
            "content": "Keep your phone with you at all times and be prepared to respond quickly to any leads or sightings."
        },
        {
            "step_title": "Be Patient and Don’t Give Up",
            "content": "Lost dogs can sometimes be found days or even weeks later. Continue searching, updating posts, and checking shelters regularly."
        }
    ],
},
           {
    "title": "What to do when your cat is lost",
    "description": "Effective steps to take immediately to locate your missing cat and bring them safely back home.",
    "paragraphs": [
        {
            "step_title": "Search Your Home and Surroundings Thoroughly",
            "content": "Cats often hide when frightened. Check inside your house carefully, including closets, under beds, behind furniture, and any small hidden spaces."
        },
        {
            "step_title": "Inspect Nearby Hiding Spots Outside",
            "content": "Look in bushes, sheds, garages, under cars, and other outdoor hiding places where your cat might seek shelter."
        },
        {
            "step_title": "Leave Familiar Scents Outside",
            "content": "Place your cat’s bedding, favorite blanket, or your worn clothing near your front door or yard to help your cat find its way back using scent."
        },
        {
            "step_title": "Notify Your Neighbors",
            "content": "Ask neighbors to check their garages, sheds, and other possible hiding spots. Provide them with a recent photo and your contact details."
        },
        {
            "step_title": "Put Up Flyers Around Your Neighborhood",
            "content": "Create flyers with a clear photo, description, and your phone number. Post them on community boards, local shops, and vet clinics."
        },
        {
            "step_title": "Use Social Media and Lost Pet Networks",
            "content": "Post about your lost cat on social media platforms, local lost-and-found pet groups, and websites dedicated to reuniting lost pets."
        },
        {
            "step_title": "Visit Local Animal Shelters and Veterinary Clinics",
            "content": "Check with animal shelters and vet clinics nearby to see if anyone has brought in a found cat matching your description."
        },
        {
            "step_title": "Search at Different Times of the Day",
            "content": "Cats are often more active and visible at dawn, dusk, or night. Try searching quietly during these times to increase your chances of spotting your cat."
        },
        {
            "step_title": "Use Food and Familiar Sounds",
            "content": "Place your cat’s favorite food outside and softly call their name or use a familiar sound, like shaking a treat bag, to attract them."
        },
        {
            "step_title": "Keep Checking and Don’t Lose Hope",
            "content": "Continue searching, updating flyers and online posts regularly. Lost cats can return after several days or weeks."
        }
    ],
}
,
            {
                "title": "Why you shouldn't leave windows open for pets",
                "description": "Risks and precautions about leaving windows open when pets are inside.",
                "paragraphs": [
                    {
                        "step_title": "Risk of escape",
                        "content": "Pets can jump out or get stuck, leading to injury or loss."
                    },
                    {
                        "step_title": "Security risks",
                        "content": "Open windows can allow intruders or other animals to enter your home."
                    },
                    {
                        "step_title": "Use proper barriers",
                        "content": "If you must leave windows open, install secure screens to protect your pets."
                    },
                ],
            },
            {
    "title": "What to Do If You Meet a Stray or Strained Dog",
    "description": "Important safety tips and steps to follow when you encounter a stray or possibly aggressive dog.",
    "paragraphs": [
        {
            "step_title": "Stay Calm and Avoid Sudden Movements",
            "content": "Do not panic or make sudden movements. Stay as calm and still as possible to avoid startling the dog."
        },
        {
            "step_title": "Do Not Stare Into the Dog’s Eyes",
            "content": "Avoid direct eye contact, as dogs may perceive this as a threat or challenge."
        },
        {
            "step_title": "Observe the Dog’s Body Language",
            "content": "Look for signs of aggression or fear, such as growling, raised hackles, bared teeth, or a tucked tail."
        },
        {
            "step_title": "Avoid Turning Your Back or Running Away",
            "content": "Running can trigger a chase instinct. Instead, back away slowly without turning your back to the dog."
        },
        {
            "step_title": "Use a Calm, Soothing Voice",
            "content": "Speak softly to the dog to try to calm it and avoid loud noises or shouting."
        },
        {
            "step_title": "Do Not Attempt to Touch or Pet the Dog Immediately",
            "content": "Let the dog come to you on its own terms if it feels safe, otherwise maintain a safe distance."
        },
        {
            "step_title": "Protect Yourself if the Dog Becomes Aggressive",
            "content": "If attacked, try to put an object like a bag or jacket between you and the dog to protect yourself."
        },
        {
            "step_title": "Look for Identification Tags",
            "content": "If safe, check if the dog is wearing a collar with contact information to help reunite it with its owner."
        },
        {
            "step_title": "Contact Animal Control or Local Shelter",
            "content": "If the dog appears lost or aggressive, call local animal control or a shelter for professional assistance."
        },
        {
            "step_title": "Avoid Feeding the Dog Immediately",
            "content": "Feeding can sometimes encourage aggressive behavior or cause dependency, so only feed if advised by professionals."
        }
    ],
},  {
        "title": "How to Prepare Your Home for a New Pet",
        "description": "A step-by-step guide to creating a safe and welcoming environment for your new furry friend.",
        "paragraphs": [
            {"step_title": "Pet-proof your home", "content": "Remove hazardous items like toxic plants, chemicals, and small objects that pets could swallow."},
            {"step_title": "Create a dedicated space", "content": "Set up a cozy area with a bed, toys, and food/water bowls to make your pet feel comfortable."},
            {"step_title": "Stock up on essentials", "content": "Have collars, leashes, food, grooming tools, and cleaning supplies ready before bringing your pet home."},
            {"step_title": "Schedule a vet appointment", "content": "Arrange an initial health check-up to establish a care plan for vaccinations and wellness."},
            {"step_title": "Learn about your pet’s breed", "content": "Understand specific needs related to activity, diet, and behavior."},
            {"step_title": "Set household rules", "content": "Decide on boundaries for your pet, like where they can sleep or play."},
            {"step_title": "Introduce slowly to family members", "content": "Help your pet acclimate by gradually introducing them to all household members."},
            {"step_title": "Prepare for training", "content": "Gather training supplies and plan basic obedience lessons to start early."},
            {"step_title": "Plan regular exercise", "content": "Ensure you have time and space for daily walks or play sessions."},
            {"step_title": "Be patient", "content": "Remember, adapting to a new home takes time for your pet."},
        ],
    },
    {
        "title": "Recognizing Signs of Stress or Anxiety in Pets",
        "description": "Learn to identify when your pet is anxious or stressed and how to help them calm down.",
        "paragraphs": [
            {"step_title": "Watch for behavioral changes", "content": "Look out for pacing, excessive barking or meowing, hiding, or aggression."},
            {"step_title": "Notice physical signs", "content": "Panting, drooling, trembling, or dilated pupils can indicate stress."},
            {"step_title": "Observe body language", "content": "Avoidance of eye contact, lowered ears, or tucked tail are common signals."},
            {"step_title": "Identify triggers", "content": "Recognize events or situations that cause stress, such as loud noises or new people."},
            {"step_title": "Provide a safe space", "content": "Create a quiet, comfortable area where your pet can retreat."},
            {"step_title": "Maintain routine", "content": "Keep feeding, walking, and play times consistent to reduce anxiety."},
            {"step_title": "Use calming products", "content": "Consider pheromone diffusers, calming collars, or anxiety wraps."},
            {"step_title": "Increase exercise", "content": "Physical activity helps reduce stress by releasing energy."},
            {"step_title": "Seek professional help", "content": "Consult a vet or animal behaviorist for persistent anxiety."},
            {"step_title": "Avoid punishment", "content": "Never scold or punish stressed pets, as this can worsen anxiety."},
        ],
    },
    {
        "title": "Basic First Aid for Pets",
        "description": "Essential first aid tips every pet owner should know to handle emergencies before reaching a vet.",
        "paragraphs": [
            {"step_title": "Stay calm", "content": "Your pet will react better if you stay calm and composed."},
            {"step_title": "Stop bleeding", "content": "Apply gentle pressure with a clean cloth to control bleeding."},
            {"step_title": "Check airway and breathing", "content": "Make sure your pet’s airway is clear and they are breathing normally."},
            {"step_title": "Perform CPR if needed", "content": "Learn pet-specific CPR techniques for emergencies."},
            {"step_title": "Treat choking", "content": "Know how to safely remove an object blocking your pet’s throat."},
            {"step_title": "Handle fractures carefully", "content": "Limit movement and use splints only if trained."},
            {"step_title": "Avoid giving human medications", "content": "Many human drugs are toxic to pets."},
            {"step_title": "Keep emergency numbers handy", "content": "Have your vet and nearest emergency clinic contacts easily accessible."},
            {"step_title": "Use a muzzle if necessary", "content": "Prevent biting when your pet is in pain, but do not use if they are vomiting or unconscious."},
            {"step_title": "Transport safely", "content": "Use a sturdy carrier or blanket to move your pet to the vet."},
        ],
    },
    {
        "title": "Seasonal Safety Tips for Pets",
        "description": "How to keep your pets safe during extreme weather conditions—summer heat, winter cold, etc.",
        "paragraphs": [
            {"step_title": "Provide fresh water", "content": "Ensure pets have constant access to clean water, especially in hot weather."},
            {"step_title": "Avoid midday walks", "content": "Exercise early morning or late evening to avoid heatstroke."},
            {"step_title": "Never leave pets in cars", "content": "Temperatures inside cars can become fatal within minutes."},
            {"step_title": "Protect paws", "content": "Use booties in winter and avoid hot pavement in summer."},
            {"step_title": "Watch for frostbite", "content": "Check ears, tails, and paws for signs of frostbite during winter."},
            {"step_title": "Limit outdoor time", "content": "Keep pets indoors during extreme weather or storms."},
            {"step_title": "Use pet-safe antifreeze", "content": "Keep harmful chemicals out of reach."},
            {"step_title": "Groom appropriately", "content": "Trim coats in summer and avoid shaving short in winter."},
            {"step_title": "Provide shelter", "content": "Ensure outdoor pets have warm, dry, insulated shelters."},
            {"step_title": "Know signs of heatstroke", "content": "Excessive panting, drooling, and lethargy need immediate vet attention."},
        ],
    },
    {
        "title": "Traveling Safely with Pets",
        "description": "Best practices for road trips, flights, and staying in pet-friendly accommodations.",
        "paragraphs": [
            {"step_title": "Use a secure carrier or restraint", "content": "Keep your pet safe and prevent distractions while driving."},
            {"step_title": "Bring familiar items", "content": "Pack toys, bedding, and food to comfort your pet."},
            {"step_title": "Plan regular breaks", "content": "Allow your pet to stretch, relieve themselves, and hydrate."},
            {"step_title": "Check pet policies", "content": "Confirm rules for airlines, hotels, or rentals before booking."},
            {"step_title": "Carry medical records", "content": "Have vaccination records and any prescriptions handy."},
            {"step_title": "Avoid feeding before travel", "content": "Prevent nausea by limiting food intake a few hours before departure."},
            {"step_title": "Never leave pets unattended", "content": "Especially in vehicles or unfamiliar places."},
            {"step_title": "Prepare for emergencies", "content": "Know the location of nearby vets or emergency clinics."},
            {"step_title": "Acclimate your pet", "content": "Familiarize them with the carrier and travel sounds ahead of time."},
            {"step_title": "Use calming aids if needed", "content": "Consult your vet about sedatives or natural calming supplements."},
        ],
    },
    {
        "title": "How to Socialize Your Puppy or Kitten",
        "description": "Effective ways to socialize young pets to help them grow into well-behaved adults.",
        "paragraphs": [
            {"step_title": "Start early", "content": "Begin socialization between 3 and 14 weeks of age for best results."},
            {"step_title": "Expose to different people", "content": "Introduce your pet to men, women, children, and people in uniforms."},
            {"step_title": "Introduce to various environments", "content": "Take your pet to parks, busy streets, and pet-friendly stores."},
            {"step_title": "Use positive reinforcement", "content": "Reward calm and confident behavior with treats and praise."},
            {"step_title": "Handle gently", "content": "Get your pet used to being touched on paws, ears, and mouth."},
            {"step_title": "Play with other animals", "content": "Arrange safe interactions with other vaccinated pets."},
            {"step_title": "Avoid overwhelming situations", "content": "Monitor your pet and remove them if they show fear or stress."},
            {"step_title": "Be consistent", "content": "Regular exposure is key to effective socialization."},
            {"step_title": "Enroll in training classes", "content": "Consider puppy or kitten socialization groups led by professionals."},
            {"step_title": "Be patient", "content": "Some pets take longer to adjust; support them calmly."},
        ],
    },
    {
        "title": "Pet Nutrition Basics",
        "description": "Understanding dietary needs for dogs, cats, and other pets to ensure a healthy life.",
        "paragraphs": [
            {"step_title": "Choose quality food", "content": "Select commercial or homemade diets with balanced nutrients."},
            {"step_title": "Feed age-appropriate diets", "content": "Puppies, adults, and seniors have different nutritional requirements."},
            {"step_title": "Avoid toxic foods", "content": "Never feed chocolate, grapes, onions, or alcohol."},
            {"step_title": "Provide fresh water", "content": "Ensure clean water is always available."},
            {"step_title": "Monitor portion sizes", "content": "Prevent obesity by following feeding guidelines."},
            {"step_title": "Introduce new foods gradually", "content": "Avoid digestive upset by slowly changing diets."},
            {"step_title": "Consider supplements carefully", "content": "Use vitamins or minerals only under vet advice."},
            {"step_title": "Watch for allergies", "content": "Note symptoms like itching, vomiting, or diarrhea after eating."},
            {"step_title": "Limit treats", "content": "Keep treats under 10% of daily calorie intake."},
            {"step_title": "Consult your vet", "content": "Discuss dietary needs during health check-ups."},
        ],
    },
    {
        "title": "How to Introduce a New Pet to Your Current Pets",
        "description": "Tips for smooth introductions and minimizing territorial conflicts.",
        "paragraphs": [
            {"step_title": "Prepare separate spaces", "content": "Set up separate areas with food, water, and beds for each pet."},
            {"step_title": "Swap scents first", "content": "Exchange bedding or toys so pets get used to each other’s smell."},
            {"step_title": "Keep initial meetings short", "content": "Supervise and gradually increase interaction time."},
            {"step_title": "Use positive reinforcement", "content": "Reward calm behavior with treats and praise."},
            {"step_title": "Avoid forcing interaction", "content": "Let pets approach each other on their own terms."},
            {"step_title": "Observe body language", "content": "Watch for signs of stress or aggression."},
            {"step_title": "Provide escape routes", "content": "Allow pets to retreat if they feel threatened."},
            {"step_title": "Maintain routines", "content": "Keep feeding and playtimes consistent to reduce stress."},
            {"step_title": "Be patient", "content": "Introductions can take days to weeks to succeed."},
            {"step_title": "Seek help if needed", "content": "Consult a behaviorist for difficult introductions."},
        ],
    },
    {
        "title": "Signs Your Pet Needs a Vet Visit",
        "description": "Know when a pet’s behavior or symptoms require professional medical attention.",
        "paragraphs": [
            {"step_title": "Changes in appetite or water intake", "content": "Eating or drinking significantly more or less than usual."},
            {"step_title": "Lethargy or weakness", "content": "Unusual tiredness or reluctance to move."},
            {"step_title": "Vomiting or diarrhea", "content": "Persistent or severe digestive issues."},
            {"step_title": "Difficulty breathing", "content": "Wheezing, coughing, or rapid breathing."},
            {"step_title": "Limping or difficulty moving", "content": "Signs of pain or injury."},
            {"step_title": "Excessive scratching or hair loss", "content": "Possible skin infections or allergies."},
            {"step_title": "Behavioral changes", "content": "Aggression, confusion, or hiding more than usual."},
            {"step_title": "Eye or nose discharge", "content": "Unusual secretions that may indicate infection."},
            {"step_title": "Swelling or lumps", "content": "New or growing bumps on the body."},
            {"step_title": "Seizures or collapse", "content": "Immediate emergency veterinary care needed."},
        ],
    },
    {
        "title": "Common Household Hazards for Pets and How to Avoid Them",
        "description": "Identify toxic plants, foods, and chemicals that can be dangerous to pets.",
        "paragraphs": [
            {"step_title": "Toxic foods", "content": "Keep chocolate, grapes, raisins, onions, garlic, and xylitol away from pets."},
            {"step_title": "Dangerous plants", "content": "Avoid poinsettias, lilies, azaleas, and philodendrons."},
            {"step_title": "Household chemicals", "content": "Store cleaners, antifreeze, and pesticides securely."},
            {"step_title": "Small objects", "content": "Keep coins, batteries, and children's toys out of reach."},
            {"step_title": "Medications", "content": "Never give human medicine to pets unless prescribed by a vet."},
            {"step_title": "Open windows and balconies", "content": "Use screens and barriers to prevent falls."},
            {"step_title": "Electrical cords", "content": "Cover or hide cords to prevent chewing."},
            {"step_title": "Garbage access", "content": "Use pet-proof bins to avoid ingestion of harmful items."},
            {"step_title": "Hot surfaces", "content": "Keep pets away from stoves, fireplaces, and heaters."},
            {"step_title": "Secure trash areas", "content": "Prevent pets from accessing spoiled or toxic food waste."},
        ],
    },

        ]

        for guide_data in guides_data:
            guide = Guide.objects.create(
                title=guide_data["title"],
                description=guide_data["description"],
                is_visible=True,
                cover_prompt="",
                cover_alt="",
                cover_caption="",
                cover_source="",
                created_by=user,
                updated_by=user,
            )

            for i, para in enumerate(guide_data["paragraphs"]):
                Paragraph.objects.create(
                    guide=guide,
                    order=i,
                    step_title=para["step_title"],
                    content=para["content"],
                    illustration_prompt="",
                    illustration_alt="",
                    illustration_caption="",
                    illustration_source="",
                    created_by=user,
                    updated_by=user,
                )

            self.stdout.write(self.style.SUCCESS(f"✅ Created guide: '{guide.title}' with {len(guide_data['paragraphs'])} paragraphs."))

        self.stdout.write(self.style.SUCCESS("🎉 Successfully populated 4 fixed guides."))
