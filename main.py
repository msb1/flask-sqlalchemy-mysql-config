import yaml
from flask import render_template, flash
from model.manage import Equip, Continuous, Discrete, Alert, db, app, csrf
from model.forms import EquipForm, ContinuousForm, DiscreteForm, AlertForm
from model.forms import DeleteEquip, DeleteContinuous, DeleteDiscrete, DeleteAlert

@app.route('/', methods=['GET', 'POST'])
def equipfxn():
    equipForm = EquipForm()
    deleteEquip = DeleteEquip()
    # Equip
    if equipForm.validate_on_submit():
        if equipForm.submit.data or equipForm.generate.data:
            equip = db.session.query(Equip).get(equipForm.eid.data)
            if not equip:
                equip = Equip(equipForm.eid.data, equipForm.name.data, equipForm.line.data, equipForm.lineid.data, 
                              equipForm.etype.data, equipForm.simulator.data, equipForm.errate.data, 
                              equipForm.success.data, equipForm.filename.data)
                db.session.add(equip)
                flash('New Equipment, {}, added!'.format(equip.name), 'success')
            else:
                equip.name = equipForm.name.data
                equip.line = equipForm.line.data
                equip.lineid = equipForm.lineid.data
                equip.etype = equipForm.etype.data
                equip.simulator = equipForm.simulator.data
                equip.errate = equipForm.errate.data
                equip.success = equipForm.success.data
                equip.filename = equipForm.filename.data
                flash('Equipment with Id {} updated!'.format(equip.eid), 'success')
            db.session.commit()
            # if generate data - write equipment to yaml file(s)
            if equipForm.generate.data:
                # generate yaml config/simulator files for submitted equipment
                cont = db.session.query(Continuous).filter_by(eid = equip.eid).all()
                disc = db.session.query(Discrete).filter_by(eid = equip.eid).all()
                alert = db.session.query(Alert).filter_by(eid = equip.eid).all()
                clist = []
                for c in cont:
                    clist.append({'id': c.cid, 'name': c.name, 'max': c.cmax, 'min': c.cmin, 'dist': c.distribution, 
                                  'pos1': c.posparam1, 'pos2': c.posparam2, 'neg1': c.negparam1, 'neg2': c.negparam2})
                dlist = []
                for d in disc:
                    dlist.append({'id': d.dd, 'name': d.name,'num': d.numlevels, 'levels': d.levels, 'pos': d.posprobs, 'neg': d.negprobs})
                alist = []
                for a in alert:
                    alist.append({'id': a.aid, 'name': a.name,'atype': a.atype, 'warn': a.warnlevel, 'alarm': a.alarmlevel, 'incr': a.increasing})
                equipconfig = {'name':equip.name, 'cont': clist, 'disc': dlist, 'alrt': alist, 'err': equip.errate, 'success': equip.success}
                config_file = open(equip.filename  + '.yml', 'w')
                yaml.dump(equipconfig, config_file)
                config_file.close()
                flash('Equipment with Id {} selected files generated!'.format(equipForm.eid.data), 'success')
                pass
    if deleteEquip.validate_on_submit() and deleteEquip.delete.data:
        db.session.query(Equip).filter_by(eid=deleteEquip.eid.data).delete()
        flash('Equipment with Id {} deleted!'.format(Equip.eid.data), 'success')
        db.session.commit()

    return render_template('admin/equip.html', title='Configuration Manager', 
                           equipForm=equipForm, deleteEquip=deleteEquip, equipment=db.session.query(Equip).all()) # noqa


@app.route('/continuous', methods=['GET', 'POST'])
def continuousfxn():
    continuousForm = ContinuousForm()
    deleteContinuous = DeleteContinuous()
    # Continuous
    if continuousForm.validate_on_submit() and continuousForm.submit.data:
        continuous = db.session.query(Continuous).get(continuousForm.cid.data)
        if not continuous:
            continuous = Continuous(continuousForm.cid.data, continuousForm.name.data, continuousForm.eid.data, 
                                        continuousForm.cmax.data, continuousForm.cmin.data, continuousForm.distribution.data, 
                                        continuousForm.posparam1.data, continuousForm.posparam2.data, 
                                        continuousForm.negparam1.data, continuousForm.negparam2.data)
            db.session.add(continuous)
            flash('New Continuous Device, {}, added!'.format(continuous.name), 'success')
        else:
            continuous.name = continuousForm.name.data
            continuous.eid = continuousForm.eid.data 
            continuous.cmax = continuousForm.cmax.data
            continuous.cmin = continuousForm.cmin.data
            continuous.distribution = continuousForm.distribution.data
            continuous.posparam1 = continuousForm.posparam1.data
            continuous.posparam2 = continuousForm.posparam2.data 
            continuous.negparam1 = continuousForm.negparam1.data
            continuous.negparam2 = continuousForm.negparam2.data
            flash('Continuous Device with Id {} updated!'.format(continuous.cid), 'success')
        db.session.commit()
    if deleteContinuous.validate_on_submit() and deleteContinuous.delete.data:
        db.session.query(Continuous).filter_by(cid=deleteContinuous.cid.data).delete()
        flash('Continuous Device with Id {} deleted!'.format(Continuous.cid.data), 'success')
        db.session.commit()

    return render_template('admin/continuous.html', title='Configuration Manager', 
                            continuousForm=continuousForm, deleteContinuous=deleteContinuous, contdevices=db.session.query(Continuous).all()) #noqa
                                

@app.route('/discrete', methods=['GET', 'POST'])
def discretefxn():
    discreteForm = DiscreteForm()
    deleteDiscrete = DeleteDiscrete()
    # Discrete
    if discreteForm.validate_on_submit() and discreteForm.submit.data:
        discrete = db.session.query(Discrete).get(discreteForm.dd.data)
        if not discrete:
            discrete = Discrete(discreteForm.dd.data, discreteForm.name.data, discreteForm.eid.data, 
                                        discreteForm.numlevels.data, discreteForm.levels.data, 
                                        discreteForm.posprobs.data, discreteForm.negprobs.data)
            db.session.add(discrete)
            flash('New Discrete Device, {}, added!'.format(discrete.name), 'success')
        else:
            discrete.name = discreteForm.name.data
            discrete.eid = discreteForm.eid.data
            discrete.numlevels = discreteForm.numlevels.data
            discrete.levels = discreteForm.levels.data
            discrete.posprobs = discreteForm.posprobs.data
            discrete.negprobs = discreteForm.negprobs.data
            flash('Discrete Device with Id {} updated!'.format(discrete.dd), 'success')
        db.session.commit()
    if deleteDiscrete.validate_on_submit() and deleteDiscrete.delete.data:
        db.session.query(Discrete).filter_by(dd=deleteDiscrete.dd.data).delete()
        flash('Discrete Device with Id {} deleted!'.format(Discrete.dd.data), 'success')
        db.session.commit()

    return render_template('admin/discrete.html', title='Configuration Manager', 
                            discreteForm=discreteForm, deleteDiscrete=deleteDiscrete, discdevices=db.session.query(Discrete).all()) # noqa
    
    
@app.route('/alert', methods=['GET', 'POST'])
def alertfxn():
    alertForm = AlertForm()
    deleteAlert = DeleteAlert()
    # Alert
    if alertForm.validate_on_submit() and alertForm.submit.data:
        alert = db.session.query(Alert).get(alertForm.aid.data)
        if not alert:
            alert = Alert(alertForm.aid.data, alertForm.name.data, alertForm.eid.data, 
                                        alertForm.atype.data, alertForm.warnlevel.data, 
                                        alertForm.alarmlevel.data, alertForm.increasing.data)
            db.session.add(alert)
            flash('New Alert, {}, added!'.format(alert.name), 'success')
        else:
            alert.name = alertForm.name.data
            alert.eid = alertForm.eid.data 
            alert.atype = alertForm.atype.data
            alert.warnlevel = alertForm.warnlevel.data
            alert.alarmlevel = alertForm.alarmlevel.data
            alert.increasing = alertForm.increasing.data
            flash('Alert with Id {} updated!'.format(alert.aid), 'success')
        db.session.commit()
    if deleteAlert.validate_on_submit() and deleteAlert.delete.data:
        db.session.query(Alert).filter_by(aid=deleteAlert.aid.data).delete()
        flash('Alert with Id {} deleted!'.format(Alert.aid.data), 'success')
        db.session.commit()

    return render_template('admin/alert.html', title='Configuration Manager', 
                            alertForm=alertForm, deleteAlert=deleteAlert, alerts=db.session.query(Alert).all()) # noqa
    
    
def main():
    app.threaded = True
    app.debug = True
    csrf.init_app(app)
    db.init_app(app)


if __name__ == "__main__":
    main()
    app.run()