from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData

from functions import *
from const import *


app = Flask(__name__)
# engine = create_engine("postgresql://postgres:shani867@localhost/Proj")
# metadata = MetaData(engine)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:shani867@localhost/Proj"
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Proj(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    proj_name = db.Column(db.String(100))
    num_scen = db.Column(db.Integer)

    num_error_OPT = db.Column(db.Integer)
    num_error_RDR = db.Column(db.Integer)
    num_error_GPS = db.Column(db.Integer)
    num_error_IMU = db.Column(db.Integer)

    type_error_OPT = db.Column(db.string(100))
    type_error_RDR = db.Column(db.string(100))
    type_error_GPS = db.Column(db.string(100))
    type_error_IMU = db.Column(db.string(100))

    data_created = db.DateTime( default=datetime.utcnow)

    def __init__(self, proj_name, num_scen, num_error_OPT, num_error_RDR, num_error_GPS, num_error_IMU, type_error_OPT, type_error_RDR, type_error_GPS, type_error_IMU):
        self.proj_name = proj_name
        self.num_scen = num_scen

        self.num_error_OPT = num_error_OPT
        self.num_error_RDR = num_error_RDR
        self.num_error_GPS = num_error_GPS
        self.num_error_IMU = num_error_IMU

        self.type_error_OPT = type_error_OPT
        self.type_error_RDR = type_error_RDR
        self.type_error_GPS = type_error_GPS
        self.type_error_IMU = type_error_IMU

    def __repr__(self):
        return '<Task %r' % self.id

def save(new_name, amount_input):
    #Inputs
    amount_input = int(amount_input)+1
    with open(f"{SCENARIO_PATH}//Projects Documantation//Scenario_Information {new_name}.txt", mode='a') as f:
        get_txt_documantation('first', new_name)
    #Loop on each other
    for x in range(0, amount_input):
        #Write the scenario number to the documantation
        get_txt_documantation('second', new_name, number_of_scenario=x)
        measurements = []
        #Creats a dataframe ith a random traj file for each measurment
        for index, measurement in enumerate(get_random_file()):
            measurements.append(create_final_format(f"{TRAJ_PATH}//{measurement}", MEASUREMENTS[index]))
        gps, rdr, opt, imu = measurements
        measurement_dict = {'GPS': gps, 'RDR': rdr, 'OPT': opt, 'IMU': imu}
        #Extract random parameters in the selected consts
        for measurement in measurement_dict:
            tstart_ave, tstart_ae, tstart_fve, tstart_fv, tstart_turn, tstart_ave, \
            tend_ave, tend_ae, tend_fve, tend_fv, azimuth, error_max = get_parameter_list()
            #Make sure start is not larger than end
            while not ((tstart_fv<tend_fv) and (tstart_ae<tend_ae) and (tstart_ave<tend_ave) and (tstart_fve<tend_fve)):
                #Extract the random parameters
                tstart_ave, tstart_ae, tstart_fve, tstart_fv, tstart_turn, tstart_ave, \
                tend_ave, tend_ae, tend_fve, tend_fv, azimuth, error_max = get_parameter_list()
                #Extract the random errors
                error_choices = get_errors()
                #Apply the errors with the parameters to each measurement
                measurement_dict[measurement], \
                errors_representation = apply_errors(measurement_dict=measurement_dict,
                                                    measurement=measurement, error_list=error_choices,
                                                    tstart_ave=tstart_ave, tstart_ae=tstart_ae, tstart_fve=tstart_fve,
                                                    tstart_fv=tstart_fv, tstart_turn=tstart_turn,
                                                    tend_ave=tend_ave, tend_ae=tend_ae, tend_fve=tend_fve,
                                                    tend_fv=tend_fv, azimuth=azimuth, error_max=error_max, t0=t0)
                #put it in the txt file
                get_txt_documantation('third', new_name, x, measurement=measurement,
                                      errors_representation=errors_representation)
                #Save the dataframes with the errors to a file
                save_file_by_measurement(measurement_dict, x, new_name)
                f.close()


@app.route('/', method=['POST', 'GET'])
def index():
    return render_template("index.html")

@app.route('/new_project/', method=['POST', 'GET'])
def new_project():
    if request.method =='POST':
        todo_proj_name = request.form['proj_name']
        todo_num_scen = request.form['num_scen']

        error_weights_amount_OPT_list = []
        error_weights_amount_RDR_list = []
        error_weights_amount_GPS_list = []
        error_weights_amount_IMU_list = []
        for x in range(10):
            error_weights_amount_OPT_list.append(float(request.form[f'num_error_OPT_{x}']))
            error_weights_amount_RDR_list.append(float(request.form[f'num_error_RDR_{x}']))
            error_weights_amount_GPS_list.append(float(request.form[f'num_error_GPS_{x}']))
            error_weights_amount_IMU_list.append(float(request.form[f'num_error_IMU_{x}']))

        error_amount_OPT = random.choices(range(0, 10), weights=error_weights_amount_OPT_list, k=1) #how many errors will accure to each measurement
        error_amount_OPT = error_amount_OPT[0]
        error_amount_RDR = random.choices(range(0, 10), weights=error_weights_amount_RDR_list, k=1)
        error_amount_RDR = error_amount_RDR[0]
        error_amount_GPS = random.choices(range(0, 10), weights=error_weights_amount_GPS_list, k=1)
        error_amount_GPS = error_amount_GPS[0]
        error_amount_IMU = random.choices(range(0, 10), weights=error_weights_amount_IMU_list, k=1)
        error_amount_IMU = error_amount_IMU[0]
        todo_num_error_OPT = error_amount_OPT
        todo_num_error_RDR = error_amount_RDR
        todo_num_error_GPS = error_amount_GPS
        todo_num_error_IMU = error_amount_IMU

        error_list = ["FV", "AE", "AVE", "FVE"]
        error_weights_type_OPT_list = []
        error_weights_type_RDR_list = []
        error_weights_type_GPS_list = []
        error_weights_type_IMU_list = []
        for x in error_list:
            error_weights_type_OPT_list.append(float(request.form[f'type_error_OPT_{x}']))
            error_weights_type_RDR_list.append(float(request.form[f'type_error_RDR_{x}']))
            error_weights_type_GPS_list.append(float(request.form[f'type_error_GPS_{x}']))
            error_weights_type_IMU_list.append(float(request.form[f'type_error_IMU_{x}']))

        error_type_OPT = random.choices(range(0, 4), weights=error_weights_type_OPT_list, k=1)  # how many errors will accure to each measurement
        error_type_OPT = error_list[error_type_OPT[0]]
        error_type_RDR = random.choices(range(0, 4), weights=error_weights_type_RDR_list, k=1)
        error_type_RDR = error_list[error_type_RDR[0]]
        error_type_GPS = random.choices(range(0, 4), weights=error_weights_type_GPS_list, k=1)
        error_type_GPS = error_list[error_type_GPS[0]]
        error_type_IMU = random.choices(range(0, 4), weights=error_weights_type_IMU_list, k=1)
        error_type_IMU = error_list[error_type_IMU[0]]
        todo_type_error_OPT = error_type_OPT
        todo_type_error_RDR = error_type_RDR
        todo_type_error_GPS = error_type_GPS
        todo_type_error_IMU = error_type_IMU

        save(todo_proj_name, todo_num_scen)

        new_task = Proj(todo_proj_name, todo_num_scen, todo_num_error_OPT, todo_num_error_RDR, todo_num_error_GPS, todo_num_error_IMU,
                        todo_type_error_OPT, todo_type_error_RDR, todo_type_error_GPS, todo_type_error_IMU)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/new_project/')

        except:
            return "There was an issue adding you project"

    else:
        tasks = Proj.query.order.by(Proj.date_created).all()
        return render_template("new_project.html", tasks=tasks)


@app.route('/new_projects/', method=['POST', 'GET'])
def new_projects():
    if request.method =='POST':
        todo_num_projs = request.form['num_projs']
        for n in range(int(todo_num_projs)):
            todo_projs_name = request.form['projs_name'] +f'{n}'
            todo_num_scens = request.form['num_scens']

            error_weights_amount_OPT_list = []
            error_weights_amount_RDR_list = []
            error_weights_amount_GPS_list = []
            error_weights_amount_IMU_list = []
            for x in range(10):
                error_weights_amount_OPT_list.append(float(request.form[f'num_errors_OPT_{x}']))
                error_weights_amount_RDR_list.append(float(request.form[f'num_errors_RDR_{x}']))
                error_weights_amount_GPS_list.append(float(request.form[f'num_errors_GPS_{x}']))
                error_weights_amount_IMU_list.append(float(request.form[f'num_errors_IMU_{x}']))

            error_amount_OPT = random.choices(range(0, 10), weights=error_weights_amount_OPT_list, k=1) #how many errors will accure to each measurement
            error_amount_OPT = error_amount_OPT[0]
            error_amount_RDR = random.choices(range(0, 10), weights=error_weights_amount_RDR_list, k=1)
            error_amount_RDR = error_amount_RDR[0]
            error_amount_GPS = random.choices(range(0, 10), weights=error_weights_amount_GPS_list, k=1)
            error_amount_GPS = error_amount_GPS[0]
            error_amount_IMU = random.choices(range(0, 10), weights=error_weights_amount_IMU_list, k=1)
            error_amount_IMU = error_amount_IMU[0]
            todo_num_error_OPT = error_amount_OPT
            todo_num_error_RDR = error_amount_RDR
            todo_num_error_GPS = error_amount_GPS
            todo_num_error_IMU = error_amount_IMU

            error_list = ["FV", "AE", "AVE", "FVE"]
            error_weights_type_OPT_list = []
            error_weights_type_RDR_list = []
            error_weights_type_GPS_list = []
            error_weights_type_IMU_list = []
            for x in error_list:
                error_weights_type_OPT_list.append(float(request.form[f'type_errors_OPT_{x}']))
                error_weights_type_RDR_list.append(float(request.form[f'type_errors_RDR_{x}']))
                error_weights_type_GPS_list.append(float(request.form[f'type_errors_GPS_{x}']))
                error_weights_type_IMU_list.append(float(request.form[f'type_errors_IMU_{x}']))

            error_type_OPT = random.choices(range(0, 4), weights=error_weights_type_OPT_list, k=1)  # how many errors will accure to each measurement
            error_type_OPT = error_list[error_type_OPT[0]]
            error_type_RDR = random.choices(range(0, 4), weights=error_weights_type_RDR_list, k=1)
            error_type_RDR = error_list[error_type_RDR[0]]
            error_type_GPS = random.choices(range(0, 4), weights=error_weights_type_GPS_list, k=1)
            error_type_GPS = error_list[error_type_GPS[0]]
            error_type_IMU = random.choices(range(0, 4), weights=error_weights_type_IMU_list, k=1)
            error_type_IMU = error_list[error_type_IMU[0]]
            todo_type_error_OPT = error_type_OPT
            todo_type_error_RDR = error_type_RDR
            todo_type_error_GPS = error_type_GPS
            todo_type_error_IMU = error_type_IMU

            save(todo_projs_name, todo_num_scens)

            new_task = Proj(todo_projs_name, todo_num_scens, todo_num_error_OPT, todo_num_error_RDR, todo_num_error_GPS, todo_num_error_IMU,
                            todo_type_error_OPT, todo_type_error_RDR, todo_type_error_GPS, todo_type_error_IMU)

            try:
                db.session.add(new_task)
                db.session.commit()


            except:
                return "There was an issue adding you project"
            return redirect('/new_projects/')
        else:
            tasks = Proj.query.order.by(Proj.date_created).all()
            return render_template("new_projects.html", tasks=tasks)

@app.route('/existing_projects/', method=['POST', 'GET'])
def existing_projects():
    if request.method == 'POST':
        todo_proj_name = request.form['proj_name']
        todo_num_scen = request.form['num_scen']
        todo_num_error = request.form['num_error']
        todo_type_error = request.form['type_error']

        new_task = Proj(todo_proj_name, todo_num_scen, todo_num_error, todo_type_error)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/existinf_projects/')
        except:
            return 'There was an issue adding your project'

    else:
        tasks = Proj.query.order_by(Proj.date_created).all()
        return render_template('existing_projects.html', tasks=tasks)

@app.route('/delete_experiment/<int:id>')
def delete_experiment(id):
    task_to_delete = Proj.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/existing_projects/')
    except:
        return 'There was a problem deleting this project'


@app.route('/update_experiment/<int:id>', methods=['POST', 'GET'])
def update_experiment(id):
    task = Proj.query.get_or_404(id)

    if request.method == 'POST':
        task.proj_name = request.form['proj_name']
        task.num_scen = request.form['num_scen']
        task.num_error = request.form['num_error']
        task.type_error = request.form['type_error']

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/existing_projects/')
    except:
        return render_template('update_experiment.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)
