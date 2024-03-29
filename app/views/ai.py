from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import sklearn
import pickle
import sklearn.ensemble
import pandas as pd
import json


class PostListCreateAPIView(APIView):
    def post(self, request):
        if request.method == 'POST':
            # Get the JSON data from the request body
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return Response({'error': 'Invalid JSON data'}, status=400)

            # Extract the TeamA and TeamB data from the JSON
            TeamA = data.get('selectedPlayerA', [])
            TeamB = data.get('selectedPlayerB', [])

            data=predict_ml(TeamA,TeamB)
        return Response(data, status=status.HTTP_200_OK)


def predict_ml(TeamA,TeamB):
    # TeamA = ['K Rahul','M Agarwal','G Maxwell','N Pooran','K Nair','J Neesham','S Khan','M Shami','S Cottrell','R Bishnoi','M Ashwin']
    # TeamB = ['J Buttler','S Smith','S Samson','R Tewatia','R Uthappa','J Archer','R Parag','T Curran','S Gopal','A Rajpoot','J Unadkat']

    BatsmenData = pd.read_csv("app/Batter_new_data.csv").values
    BowlerData = pd.read_csv("app/Bowler_new_data.csv").values

    Batters = ['M Agarwal', 'L Livingstone', 'S Khan', 'S Dhawan', 'J Bairstow', 'P Singh', 'R Dhawan', 'B Rajapaksa', 'B Howell', 'P Mankad', 'J Sharma', 'K Williamson', 'N Pooran', 'R Tripathi', 'A Sharma', 'A Samad', 'A Markram', 'G Phillips', 'V Vinod', 'P Garg', 'S Singh', 'R Samarth', 'S Samson', 'J Buttler', 'S Hetmyer', 'D Padikkal', 'Y Jaiswal', 'R Parag', 'K Nair', 'R Dussen', 'D Mitchell', 'D Jurel', 'S Garhwal', 'V Kohli', 'G Maxwell', 'F Plessis', 'D Karthik', 'A Rawat', 'S Rutherford', 'M Lomror', 'F Allen', 'S Prabhudessai', 'L Sisodia', 'R Sharma', 'I Kishan', 'S Yadav', 'K Pollard', 'D Brevis', 'T Varma', 'F Allen', 'S Yadav', 'R Singh', 'A Singh', 'A Juyal', 'R Buddhi', 'R Jadeja', 'M Dhoni', 'M Ali', 'A Rayudu', 'R Gaikwad', 'S Dube', 'R Uthappa', 'D Conway', 'N Jagadeesan', 'S Senapati', 'B Varma', 'H Nishaanth', 'S Iyer', 'A Russell', 'N Rana', 'V Iyer', 'S Billings', 'A Hales', 'A Rahane', 'S Jackson', 'R Singh', 'A Tomar', 'P Singh', 'R Kumar', 'B Indrajith', 'R Pant', 'P Shaw', 'M Marsh', 'D Warner', 'R Powell', 'S Bharat', 'M Singh', 'Y Dhull', 'T Seifert', 'A Hebbar', 'R Patel', 'S Khan', 'K Rahul', 'M Stoinis', 'Q Kock', 'D Hooda', 'M Pandey', 'E Lewis', 'K Mayers', 'A Badoni', 'M Vohra', 'H Pandya', 'S Gill', 'D Miller', 'A Manohar', 'M Wade', 'J Roy', 'W Saha', 'V Shankar', 'S Sudharsan', 'M Henriques', 'Y Singh', 'B Cutting', 'N Ojha', 'B Sharma', 'A Nehra', 'C Gayle', 'T Head', 'K Jadhav', 'S Watson', 'S Baby', 'S Binny', 'S Aravind', 'A Choudhary', 'S Smith', 'B Stokes', 'M Tiwary', 'R Bhatia', 'A Zampa', 'A Dinda', 'I Tahir', 'P Patel', 'M McClenaghan', 'B McCullum', 'S Raina', 'A Finch', 'K Karthik', 'D Smith', 'M Gony', 'P Kumar', 'S Jakati', 'D Kulkarni', 'S Kaushik', 'G Gambhir', 'C Lynn', 'Y Pathan', 'C Woakes', 'P Chawla', 'H Amla', 'M Sharma', 'D Christian', 'P Negi', 'I Abdulla', 'B Stanlake', 'A Tare', 'C Morris', 'C Brathwaite', 'A Mishra', 'Z Khan', 'H Singh', 'S Malinga', 'A Villiers', 'C Anderson', 'C Grandhomme', 'I Sharma', 'S Badree', 'A Tye', 'E Morgan', 'M Patel', 'B Sran', 'A Mathews', 'S Marsh', 'G Singh', 'S Hasan', 'J Faulkner', 'M Johnson', 'A Nath', 'S Agarwal', 'N Singh', 'A Soni', 'M Guptill', 'A Bawne', 'I Pathan', 'M Samuels', 'L Simmons', 'M Henry', 'S Tiwary', 'I Jaggi', 'K Khejroliya', 'C Munro', 'D Short', 'B Laughlin', 'T Curran', 'A Dananjaya', 'M Vijay', 'H Klaasen', 'R Bhui', 'L Plunkett', 'J Duminy', 'I Sodhi', 'D Shorey', 'M Krishna', 'S Goswami', 'P Chopra', 'J Scantlebury-Searles', 'S Lamichhane', 'C Dala', 'C Ingram', 'K Paul', 'R Salam', 'S Curran', 'G Viljoen', 'C Varun', 'N Naik', 'G Vihari', 'P Barman', 'S Kuggeleijn', 'S Midhun', 'H Gurney', 'S Lad', 'J Denly', 'A Turner', 'D Steyn', 'Y Raj', 'O Thomas', 'S Warrier', 'J Pattinson', 'S Cottrell', 'J Philippe', 'I Udana', 'A Carey', 'T Banton', 'C Green', 'M Kumar', 'R Patidar', 'K Jamieson', 'J Richardson', 'V Singh', 'J Saxena', 'L Meriwala', 'K Richardson', 'D Malan', 'K Bharat', 'P Silva', 'A Rashid', 'T Shamsi', 'G Garton', 'P Rajapaksa', 'P Chameera', 'B Sudharsan', 'H Dussen', 'H Rana', 'K Kartikeya', 'T Stubbs', 'M Pathirana', 'R Yadav', 'M Henriques', 'Y Singh', 'B Cutting', 'N Ojha', 'B Sharma', 'A Nehra', 'C Gayle', 'T Head', 'K Jadhav', 'S Watson', 'S Baby', 'S Binny', 'S Aravind', 'A Choudhary', 'S Smith', 'B Stokes', 'M Tiwary', 'R Bhatia', 'A Zampa', 'A Dinda', 'I Tahir', 'P Patel', 'M McClenaghan', 'B McCullum', 'S Raina', 'A Finch', 'K Karthik', 'D Smith', 'M Gony', 'P Kumar', 'S Jakati', 'D Kulkarni', 'S Kaushik', 'G Gambhir', 'C Lynn', 'Y Pathan', 'C Woakes', 'P Chawla', 'H Amla', 'M Sharma', 'D Christian', 'P Negi', 'I Abdulla', 'B Stanlake', 'A Tare', 'C Morris', 'C Brathwaite', 'A Mishra', 'Z Khan', 'H Singh', 'S Malinga', 'A Villiers', 'C Anderson', 'C Grandhomme', 'I Sharma', 'S Badree', 'A Tye', 'E Morgan', 'M Patel', 'B Sran', 'A Mathews', 'S Marsh', 'G Singh', 'S Hasan', 'J Faulkner', 'M Johnson', 'A Nath', 'S Agarwal', 'N Singh', 'A Soni', 'M Guptill', 'A Bawne', 'I Pathan', 'M Samuels', 'L Simmons', 'M Henry', 'S Tiwary', 'I Jaggi', 'K Khejroliya', 'C Munro', 'D Short', 'B Laughlin', 'T Curran', 'A Dananjaya', 'M Vijay', 'H Klaasen', 'R Bhui', 'L Plunkett', 'J Duminy', 'I Sodhi', 'D Shorey', 'M Krishna', 'S Goswami', 'P Chopra', 'J Scantlebury-Searles', 'S Lamichhane', 'C Dala', 'C Ingram', 'K Paul', 'R Salam', 'S Curran', 'G Viljoen', 'C Varun', 'N Naik', 'G Vihari', 'P Barman', 'S Kuggeleijn', 'S Midhun', 'H Gurney', 'S Lad', 'J Denly', 'A Turner', 'D Steyn', 'Y Raj', 'O Thomas', 'S Warrier', 'J Pattinson', 'S Cottrell', 'J Philippe', 'I Udana', 'A Carey', 'T Banton', 'C Green', 'M Kumar', 'R Patidar', 'K Jamieson', 'J Richardson', 'V Singh', 'J Saxena', 'L Meriwala', 'K Richardson', 'D Malan', 'K Bharat', 'P Silva', 'A Rashid', 'T Shamsi', 'G Garton', 'P Rajapaksa', 'P Chameera', 'B Sudharsan', 'H Dussen', 'H Rana', 'K Kartikeya', 'T Stubbs', 'M Pathirana', 'R Yadav', 'Y Singh', 'N Ojha', 'C Gayle', 'T Head', 'K Jadhav', 'S Watson', 'S Baby', 'S Binny', 'S Smith', 'B Stokes', 'M Tiwary', 'P Patel', 'B McCullum', 'S Raina', 'A Finch', 'K Karthik', 'S Kaushik', 'G Gambhir', 'C Lynn', 'P Chawla', 'P Negi', 'A Mishra', 'H Singh', 'A Villiers', 'C Grandhomme', 'E Morgan', 'B Sran', 'A Mathews', 'M Johnson', 'A Soni', 'M Guptill', 'M Samuels', 'M Henry', 'S Tiwary', 'C Munro', 'M Vijay', 'R Bhui', 'L Plunkett', 'J Duminy', 'D Shorey', 'J Scantlebury-Searles', 'C Ingram', 'K Paul', 'R Salam', 'S Curran', 'C Varun', 'G Vihari', 'S Midhun', 'H Gurney', 'A Turner', 'Y Raj', 'J Pattinson', 'J Philippe', 'A Carey', 'R Patidar', 'D Malan', 'T Shamsi', 'G Garton', 'P Rajapaksa', 'H Dussen', 'T Stubbs']
    Bowlers = ['K Rabada', 'O Smith', 'R Chahar', 'A Singh', 'H Brar', 'V Arora', 'R Bawa', 'N Ellis', 'S Sharma', 'I Porel', 'A Taide', 'A Patel', 'W Chatterjee', 'B Singh', 'W Sundar', 'R Shepherd', 'B Kumar', 'M Jansen', 'U Malik', 'T Natarajan', 'K Tyagi', 'S Abbott', 'S Gopal', 'F Farooqi', 'S Dubey', 'J Suchith', 'P Krishna', 'T Boult', 'Y Chahal', 'R Ashwin', 'N Saini', 'N Coulter-Nile', 'J Neesham', 'O McCoy', 'K Cariappa', 'T Baroka', 'K Yadav', 'K Sen', 'A Singh', 'H Patel', 'W Hasaranga', 'J Hazlewood', 'M Siraj', 'S Ahmed', 'D Willey', 'J Behrendorff', 'S Kaul', 'K Sharma', 'C Milind', 'A Gautam', 'A Deep', 'J Bumrah', 'T David', 'J Archer', 'D Sams', 'M Ashwin', 'T Mills', 'J Unadkat', 'R Meredith', 'M Markande', 'B Thampi', 'A Tendulkar', 'A Khan', 'H Shokeen', 'D Chahar', 'D Bravo', 'C Jordan', 'M Santner', 'A Milne', 'R Hangargekar', 'P Solanki', 'M Theekshana', 'D Pretorius', 'K Asif', 'T Deshpande', 'S Singh', 'M Choudhary', 'V Chakravarthy', 'S Mavi', 'P Cummins', 'S Narine', 'U Yadav', 'T Southee', 'M Nabi', 'A Sharma', 'C Karunaratne', 'A Roy', 'R Dar', 'A Khan', 'S Thakur', 'A Patel', 'A Nortje', 'K Ahmed', 'C Sakariya', 'K Yadav', 'M Rahman', 'K Nagarkoti', 'L Yadav', 'L Ngidi', 'P Dubey', 'V Ostwal', 'A Khan', 'J Holder', 'K Pandya', 'M Wood', 'R Bishnoi', 'D Chameera', 'K Gowtham', 'S Nadeem', 'A Rajpoot', 'M Khan', 'K Sharma', 'M Yadav', 'R Khan', 'L Ferguson', 'R Tewatia', 'M Shami', 'Y Dayal', 'R Kishore', 'A Joseph', 'J Yadav', 'D Drakes', 'V Aaron', 'G Mann', 'N Ahmad', 'D Nalkande', 'P Sangwan', 'M Henriques', 'B Cutting', 'B Sharma', 'A Nehra', 'S Aravind', 'A Choudhary', 'R Bhatia', 'A Zampa', 'A Dinda', 'I Tahir', 'M McClenaghan', 'D Smith', 'M Gony', 'P Kumar', 'S Jakati', 'D Kulkarni', 'Y Pathan', 'C Woakes', 'H Amla', 'M Sharma', 'D Christian', 'I Abdulla', 'B Stanlake', 'A Tare', 'C Morris', 'C Brathwaite', 'Z Khan', 'S Malinga', 'C Anderson', 'I Sharma', 'S Badree', 'A Tye', 'M Patel', 'S Marsh', 'G Singh', 'S Hasan', 'J Faulkner', 'A Nath', 'S Agarwal', 'N Singh', 'A Bawne', 'I Pathan', 'L Simmons', 'I Jaggi', 'K Khejroliya', 'D Short', 'B Laughlin', 'T Curran', 'A Dananjaya', 'H Klaasen', 'I Sodhi', 'M Krishna', 'S Goswami', 'P Chopra', 'S Lamichhane', 'C Dala', 'G Viljoen', 'N Naik', 'P Barman', 'S Kuggeleijn', 'S Lad', 'J Denly', 'D Steyn', 'O Thomas', 'S Warrier', 'S Cottrell', 'I Udana', 'T Banton', 'C Green', 'M Kumar', 'K Jamieson', 'J Richardson', 'V Singh', 'J Saxena', 'L Meriwala', 'K Richardson', 'K Bharat', 'P Silva', 'A Rashid', 'P Chameera', 'B Sudharsan', 'H Rana', 'K Kartikeya', 'M Pathirana', 'R Yadav']

    BatDict = {}
    BowlDict = {}

    for i in BatsmenData:
        BatDict[i[0]] = i

    for i in BowlerData:
        BowlDict[i[0]] = i

    # print(BatDict)

    TeamBatters = []
    TeamBowlers = []

    for i in TeamA:
        if i in Batters:
            TeamBatters.append(BatDict[i])
        else:
            TeamBowlers.append(BowlDict[i])

    for i in TeamB:
        if i in Batters:
            TeamBatters.append(BatDict[i])
        else:
            TeamBowlers.append(BowlDict[i])

    # print(TeamBatters, TeamBowlers)

    Test_bat = pd.DataFrame(data = TeamBatters, columns = ['Player','Mat','Inns','Runs','HS','Ave','BF','SR','100','50','0','4s','6s'])
    Test_bowl = pd.DataFrame(data = TeamBowlers, columns = ['Player','Mat','Inns','Overs','Mdns','Runs','Wkts','Ave','Econ','SR','4','5'])

    # print(Test_bat)

    
    file1 = "app/Saved_Models/bat_model.pickle"
    bat_model = pickle.load(open(file1,"rb"))

    file2 = "app/Saved_Models/bowl_model.pickle"
    bowl_model = pickle.load(open(file2,"rb"))

    file3 = "app/Saved_Models/pipeline_bat.pickle"
    pipe_bat = pickle.load(open(file3,"rb"))

    file4 = "app/Saved_Models/pipeline_bowl.pickle"
    pipe_bowl = pickle.load(open(file4,"rb"))






    X_bat = Test_bat[['Mat','Inns','Runs','HS','Ave','BF','SR','100','50','0','4s','6s']]
    X_bowl = Test_bowl[['Mat','Inns','Overs','Mdns','Runs','Wkts','Ave','Econ','SR','4','5']]

    X_transformed_bat = pipe_bat.transform(X_bat)
    X_transformed_bowl = pipe_bowl.transform(X_bowl)

    y_bat = bat_model.predict(X_transformed_bat)

    y_bowl = bowl_model.predict(X_transformed_bowl)
    

    InD11 = []

    for i in range (len(y_bat)):
        if y_bat[i] == 1:
            InD11.append(Test_bat.values[i][0])

    for i in range(len(y_bowl)):
        if y_bowl[i] == 1:
            InD11.append(Test_bowl.values[i][0])

    # print(InD11, len(InD11))


    all = TeamA + TeamB

    diff = (11 - len(InD11)) if len(InD11) < 11 else 0
    # print(diff)
    for i in all:
        if diff != 0 and i not in InD11:
            InD11.append(i)
            diff -= 1


    output = InD11[:11]    
    # print(output)       
    return output
    # return Response(output, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)