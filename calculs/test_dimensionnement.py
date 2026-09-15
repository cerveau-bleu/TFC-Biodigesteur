"""Tests de conservation, domaine et comparaison aux valeurs imprimées."""
import unittest
from dataclasses import replace
from math import inf
from dimensionnement import Parametres, calculer, white_darcy, temps_chauffe_s


class Verification(unittest.TestCase):
    def test_valeurs_imprimees(self):
        r = calculer()
        for nom, ref, tol in [('volume_utile_m3',.513385,.000001),
            ('K_enveloppe_W_K',3.00250,.00001),('puissance_consigne_W',296.30,.02),
            ('demarrage_h',20.35,.02),('recuperation_h',1.38,.01),
            ('dp_total_Pa',3490.5,.2)]:
            self.assertAlmostEqual(r[nom],ref,delta=tol,msg=nom)

    def test_conservations(self):
        p=Parametres(); r=calculer(p)
        self.assertAlmostEqual(r['volume_total_m3'],r['volume_gaz_m3']+r['volume_utile_m3']+r['volume_tube_m3'])
        self.assertAlmostEqual(r['puissance_consigne_W'],r['C_eau_W_K']*(p.entree_eau_C-r['sortie_eau_C']))
        self.assertAlmostEqual(r['demarrage_chaleur_recue_kWh'],r['demarrage_sensible_kWh']+r['demarrage_pertes_kWh'],places=9)

    def test_white_exemple_documentation(self):
        # L'exemple illustratif de fluids a di/Ds=0.2 : hors plage déclarée.
        # Notre wrapper doit le refuser plutôt qu'extrapoler silencieusement.
        with self.assertRaises(ValueError):
            white_darcy(250,.02,.1)

    def test_integration_independante(self):
        # RK4 indépendant de la formule logarithmique, pas de 60 secondes.
        p=Parametres(); r=calculer(p)
        T=p.initiale_C; t=0.; fin=r['demarrage_h']*3600
        def derivee(x):
            return (r['G_W_K']*(p.entree_eau_C-x)-r['K_enveloppe_W_K']*(x-p.ambiance_C))/r['capacite_J_K']
        while t < fin:
            h=min(60.,fin-t)
            a=derivee(T); b=derivee(T+h*a/2); c=derivee(T+h*b/2); d=derivee(T+h*c)
            T+=h*(a+2*b+2*c+d)/6; t+=h
        self.assertAlmostEqual(T,p.consigne_C,places=8)

    def test_limite_sans_pertes(self):
        self.assertAlmostEqual(temps_chauffe_s(100,10,0,40,0,20,30),6.931471805599453)
        self.assertEqual(temps_chauffe_s(100,1,10,45,20,20,35),inf)

    def test_rejet_entrees_invalides(self):
        for changements in [{'tube_interieur_m':.02},{'rho_b_kg_m3':-1},{'fraction_gaz':1},{'debit_eau_L_min':60},{'hb_W_m2K':float('nan')}]:
            with self.assertRaises(ValueError):
                calculer(replace(Parametres(),**changements))

    def test_tendances(self):
        nominal=calculer()
        self.assertGreater(calculer(replace(Parametres(),hb_W_m2K=20))['demarrage_h'],nominal['demarrage_h'])
        self.assertLess(calculer(replace(Parametres(),isolant_m=.10))['pertes_enveloppe_W'],nominal['pertes_enveloppe_W'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
