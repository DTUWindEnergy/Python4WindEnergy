//  Omnivor
int  io_init(const char*);
int  io_init_open(const char*);
void io_term();
int  check();
void error_solved();
void io_set_var(const char*,double*);
void io_set_svar(const char*,const char*);
void io_get_svar(const char*, char*,int*);
void io_get_version(char*);
int  it_incrementtime();
void it_resettime();

// User Velocity
void iv_user_vel_init(int*nFields_in);
void iv_user_vel_add_from_v1v2v3(double*v1,double*v2,double*v3,int*bComputeGrad,int*bPolar,int*n1,int*n2,int*n3);
void iv_user_vel_get(int*ifield,int*ncps,double*CPs,double*Utot,double*Grad);
void iv_user_vel_term();
// User Velocity, provided by mouffette
void iv_user_vel_compute();
void iv_user_vel_export(const char*);

// Wind
void iw_getfreewind(double*);
void iw_setfreewind(double*);

// Mouffette
void im_set_algo_var(const char*, double*);
void im_set_algo_vec(const char*, double*);
void im_get_wing_var(double*,const char*, int*,int*);
void im_get_wing_vec(double*,const char*, int*,int*);
void im_patch_get_loads(int*,int*,int*,double*,double*,double*,double*,double*);
void im_wing_get_loads(int*,int*,double*,double*,double*,double*);
void im_wing_set_gamma(int*,int*,double*,double*);
void im_get_panl_loads(int*,double*,double*,double*,double*,double*,double*);
// Raccoon Main
int ir_init();
int ir_apply();
void ir_term();
void ir_dotimestep();
void ir_finalize1();
void ir_finalize2();
void ir_loadscalc();
void ir_export(int*);
void ir_addmiscelement();
void ir_gridvelocity();
void ir_savestate();
void ir_loadstate(const char*);
void ir_dotimeloop();
void ir_set_nbodies(int*nb,int*nw);
void ir_new_obj(const char*);
void ir_add_obj();
void ir_set_obj_var(const char*,double*);
void ir_set_obj_str(const char*,const char*);
void ir_set_obj_lnk(int*ibParent,double*PO_p,double*T_b2p);
void ir_set_obj_pos(double*ShiftVect,double*RotMatrix);
void ir_set_obj_file(const char*,const char*,const char*,int*);
void ir_set_obj_vel(double*TranslatVel,double*RotVect,double*RotCenter,double*RotVel,double*RotPhase);
