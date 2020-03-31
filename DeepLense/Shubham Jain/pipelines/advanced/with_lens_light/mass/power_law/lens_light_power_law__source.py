import autofit as af
import autolens as al

# In this pipeline, we fit the mass of a strong lens using a power-law + shear model.

# The lens light, mass model and source are initialized using already run 'source' and 'light' pipelines.

# The pipeline is one phases:

# Phase 1:

# Fit the lens mass model as a power-law, using the source model from a previous pipeline.
# Lens Mass: Light + EllipticalPowerLaw + ExternalShear
# Source Light: Previous Pipeline Source.
# Previous Pipelines: no_lens_light/source/*/lens_sie__source_*py
# Prior Passing: Lens Mass (model -> previous pipeline), source (model / instance -> previous pipeline)
# Notes: If the source is parametric, its parameters are varied, if its an inversion, they are fixed.


def source_is_inversion_from_setup(setup):
    if setup.source.type_tag in "sersic":
        return False
    else:
        return True


def lens_with_previous_light_and_model_mass(setup):
    """Setup the lens galaxy model using the previous pipeline or phases results.

    This function is required because the lens light model is not specified by the pipeline itself (e.g. the previous
    pipeline determines if the lens light was modeled as a Sersic, bulge-disk, Gaussians, etc.)

    So, we have to pass the lens light to this pipeline without explicitly referencing its light components."""

    if setup.mass.fix_lens_light:
        lens = af.last.instance.galaxies.lens
    else:
        lens = af.last.model.galaxies.lens

    lens.hyper_galaxy = (
        af.last.result.hyper_combined.instance.optional.galaxies.lens.hyper_galaxy
    )

    return lens


def source_with_previous_model_or_instance(setup):
    """Setup the source source model using the previous pipeline or phase results.

    This function is required because the source light model is not specified by the pipeline itself (e.g. the previous
    pipelines determines if the source was modeled using parametric light profiles or an inversion.

    If the source was parametric this function returns the source as a model, given that a parametric source should be
    fitted for simultaneously with the mass model.

    If the source was an inversion then it is returned as an instance, given that the inversion parameters do not need
    to be fitted for alongside the mass model.

    The bool include_hyper_source determines if the hyper-galaxy used to scale the sources noises is included in the
    model fitting.
    """
    if setup.general.hyper_galaxies:

        hyper_galaxy = af.PriorModel(al.HyperGalaxy)

        hyper_galaxy.noise_factor = (
            af.last.hyper_combined.model.galaxies.source.hyper_galaxy.noise_factor
        )
        hyper_galaxy.contribution_factor = (
            af.last.hyper_combined.instance.optional.galaxies.source.hyper_galaxy.contribution_factor
        )
        hyper_galaxy.noise_power = (
            af.last.hyper_combined.instance.optional.galaxies.source.hyper_galaxy.noise_power
        )

    else:

        hyper_galaxy = None

    if setup.source.type_tag in "sersic":

        return al.GalaxyModel(
            redshift=af.last.instance.galaxies.source.redshift,
            sersic=af.last.model.galaxies.source.sersic,
            hyper_galaxy=hyper_galaxy,
        )

    else:

        return al.GalaxyModel(
            redshift=af.last.instance.galaxies.source.redshift,
            pixelization=af.last.hyper_combined.instance.galaxies.source.pixelization,
            regularization=af.last.hyper_combined.instance.galaxies.source.regularization,
            hyper_galaxy=hyper_galaxy,
        )


def make_pipeline(
    setup,
    phase_folders=None,
    redshift_lens=0.5,
    redshift_source=1.0,
    positions_threshold=None,
    sub_size=2,
    signal_to_noise_limit=None,
    bin_up_factor=None,
    pixel_scale_interpolation_grid=None,
    inversion_uses_border=True,
    inversion_pixel_limit=None,
):

    ### SETUP PIPELINE & PHASE NAMES, TAGS AND PATHS ###

    # A source tag distinguishes if the previous pipeline models used a parametric or inversion model for the source.

    pipeline_name = "pipeline_mass__power_law"

    # For pipeline tagging we need to set the mass type
    setup.set_mass_type(mass_type="power_law")

    # This pipeline is tagged according to whether:

    # 1) Hyper-fitting setup (galaxies, sky, background noise) are used.
    # 2) The lens galaxy mass model includes an external shear.
    # 3) The lens's light model is fixed or variable.

    phase_folders.append(pipeline_name)
    phase_folders.append(setup.general.tag)
    phase_folders.append(setup.source.tag)
    phase_folders.append(setup.light.tag)
    phase_folders.append(setup.mass.tag)

    ### SETUP SHEAR ###

    # Include the shear in the mass model if not switched off in the pipeline setup.

    if not setup.mass.no_shear:
        if af.last.model.galaxies.lens.shear is not None:
            shear = af.last[-1].model.galaxies.lens.shear
        else:
            shear = al.mp.ExternalShear
    else:
        shear = None

    ### PHASE 1 ###

    # In phase 1, we fit the lens galaxy's light and mass and one source galaxy, where we:

    # 1) Use the source galaxy of the 'source' pipeline.
    # 2) Use the lens galaxy light of the 'light' pipeline.
    # 3) Set priors on the lens galaxy mass using the EllipticalIsothermal and ExternalShear of previous pipelines.

    # Setup the lens using the light model the 'light' pipeline, which will be fixed or fitted for depending on
    # the fix_lens_light parameter

    # Setup the power-law mass profile and initialize its priors from the SIE.

    # lens = lens_with_previous_light_and_model_mass(setup=setup)

    mass = af.PriorModel(al.mp.EllipticalPowerLaw)

    # -1 as the last phase was the light phase, with a fixed mass model.

    mass.centre = af.last[-1].model.galaxies.lens.mass.centre
    mass.axis_ratio = af.last[-1].model.galaxies.lens.mass.axis_ratio
    mass.phi = af.last[-1].model.galaxies.lens.mass.phi
    mass.einstein_radius = (
        af.last[-1].model_absolute(a=0.3).galaxies.lens.mass.einstein_radius
    )

    # lens.mass = mass
    # lens.shear = shear

    if setup.mass.fix_lens_light:

        lens = al.GalaxyModel(
            redshift=redshift_lens,
            bulge=af.last.instance.galaxies.lens.bulge,
            disk=af.last.instance.galaxies.lens.disk,
            mass=mass,
            shear=shear,
            hyper_galaxy=af.last.hyper_combined.instance.optional.galaxies.lens.hyper_galaxy,
        )

    else:

        lens = al.GalaxyModel(
            redshift=redshift_lens,
            bulge=af.last.model.galaxies.lens.bulge,
            disk=af.last.model.galaxies.lens.disk,
            mass=mass,
            shear=shear,
            hyper_galaxy=af.last.hyper_combined.instance.optional.galaxies.lens.hyper_galaxy,
        )

    # Setup the source model, which uses a variable parametric profile or fixed inversion model depending on the
    # previous pipeline.

    # TODO : Pretty sure this function is broken, and works simply cause .model is the default.

    source = source_with_previous_model_or_instance(setup=setup)

    phase1 = al.PhaseImaging(
        phase_name="phase_1__lens_power_law__source",
        phase_folders=phase_folders,
        galaxies=dict(len=lens, source=source),
        hyper_image_sky=af.last.hyper_combined.instance.optional.hyper_image_sky,
        hyper_background_noise=af.last.hyper_combined.instance.optional.hyper_background_noise,
        positions_threshold=positions_threshold,
        sub_size=sub_size,
        signal_to_noise_limit=signal_to_noise_limit,
        bin_up_factor=bin_up_factor,
        pixel_scale_interpolation_grid=pixel_scale_interpolation_grid,
        inversion_uses_border=inversion_uses_border,
        inversion_pixel_limit=inversion_pixel_limit,
        optimizer_class=af.MultiNest,
    )

    phase1.optimizer.const_efficiency_mode = True
    phase1.optimizer.n_live_points = 75
    phase1.optimizer.sampling_efficiency = 0.2
    phase1.optimizer.evidence_tolerance = 0.8

    # If the source is parametric, the inversion hyper phase below will be skipped.

    phase1 = phase1.extend_with_multiple_hyper_phases(
        inversion=source_is_inversion_from_setup(setup=setup),
        hyper_galaxy=setup.general.hyper_galaxies,
        include_background_sky=setup.general.hyper_image_sky,
        include_background_noise=setup.general.hyper_background_noise,
    )

    return al.PipelineDataset(pipeline_name, phase1)
